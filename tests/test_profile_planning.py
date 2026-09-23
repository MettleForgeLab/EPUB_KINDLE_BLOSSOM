from __future__ import annotations

import json

from PIL import Image
import pytest

from mfl_adapter.profile_planning import (
    plan_component,
    plan_profile,
)


def plate_component():
    return {
        "key":"test-plate",
        "route":"MEDIUM PLATE",
        "reason":"test",
        "source_width_px":2000,
        "display_width_percent":72,
        "byte_budget":250000,
    }


def test_live_component_is_not_forced_into_plate_planning():
    result=plan_component({
        "key":"live-test",
        "route":"SIMPLIFY LIVE",
        "reason":"ordered relation",
    })

    assert result["planning_status"] == "NOT APPLICABLE"


def test_profile_plate_meets_scribe_reserve():
    result=plan_component(
        plate_component(),
        device_keys=("scribe-3",),
    )

    assert result["planning_status"] == "RESERVE MET"
    assert result["minimum_source_width_for_reserve_px"] == 1788
    assert result["byte_status"] == "NOT MEASURED"


def test_completed_run_enriches_dimensions_and_bytes(tmp_path):
    run=tmp_path/"run"
    plates=run/"plates"
    plates.mkdir(parents=True)

    path=plates/"test-plate.png"

    Image.new(
        "RGB",
        (2000,1500),
        (255,255,255),
    ).save(path)

    result=plan_component(
        plate_component(),
        run_dir=run,
        device_keys=("scribe-3",),
    )

    assert result["actual_plate"]["width_px"] == 2000
    assert result["actual_plate"]["height_px"] == 1500
    assert result["actual_plate"]["bytes"] == path.stat().st_size
    assert result["byte_status"] == "WITHIN BUDGET"


def test_rendered_width_must_match_profile(tmp_path):
    run=tmp_path/"run"
    plates=run/"plates"
    plates.mkdir(parents=True)

    Image.new(
        "RGB",
        (1900,1500),
        (255,255,255),
    ).save(plates/"test-plate.png")

    with pytest.raises(
        ValueError,
        match="does not match profile source_width_px",
    ):
        plan_component(
            plate_component(),
            run_dir=run,
            device_keys=("scribe-3",),
        )


def test_plan_profile_uses_existing_component_schema(tmp_path):
    profile={
        "profile_id":"test-profile",
        "profile_version":"1",
        "mode":"test",
        "components":[
            plate_component(),
            {
                "key":"live-test",
                "route":"SIMPLIFY LIVE",
                "reason":"ordered",
            },
        ],
    }

    path=tmp_path/"profile.json"
    path.write_text(
        json.dumps(profile),
        encoding="utf-8",
    )

    result=plan_profile(
        path,
        device_keys=("scribe-3",),
    )

    assert result["summary"]["component_count"] == 2
    assert result["summary"]["plate_count"] == 1
    assert result["components"][0]["key"] == "test-plate"
    assert result["components"][1]["planning_status"] == "NOT APPLICABLE"

def test_byte_budget_status_distinguishes_near_from_within():
    from mfl_adapter.profile_planning import byte_budget_status

    status,utilization=byte_budget_status(
        211570,
        220000,
    )

    assert status == "NEAR BUDGET"
    assert 0.96 < utilization < 0.97


def test_byte_budget_overage_is_a_finding_not_resolution_failure():
    from mfl_adapter.profile_planning import (
        build_findings,
    )

    plan={
        "components":[
            {
                "key":"plate",
                "planning_status":"RESERVE MET",
                "byte_status":"OVER BUDGET",
            }
        ]
    }

    findings=build_findings(plan)

    assert len(findings) == 1
    assert findings[0]["kind"] == "image-weight"
    assert findings[0]["level"] == "WARNING"


def test_underresolved_pre_render_plan_stops():
    from mfl_adapter.profile_planning import (
        require_pre_render_resolved,
    )

    plan={
        "components":[
            {
                "key":"too-small",
                "planning_status":"UNDER-RESOLVED",
            }
        ]
    }

    with pytest.raises(
        ValueError,
        match="too-small",
    ):
        require_pre_render_resolved(plan)


def test_reserve_met_pre_render_plan_proceeds():
    from mfl_adapter.profile_planning import (
        require_pre_render_resolved,
    )

    plan={
        "components":[
            {
                "key":"healthy",
                "planning_status":"RESERVE MET",
            },
            {
                "key":"live",
                "planning_status":"NOT APPLICABLE",
            },
        ]
    }

    assert require_pre_render_resolved(plan) is None
