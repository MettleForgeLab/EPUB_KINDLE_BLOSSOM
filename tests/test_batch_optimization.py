from __future__ import annotations

import json

from PIL import Image
import pytest

from mfl_adapter.batch_optimization import (
    run_batch_optimization_lab,
)


def make_fixture(tmp_path):
    profile={
        "profile_id":"batch-test",
        "profile_version":2,
        "components":[
            {
                "key":"plate-a",
                "route":"MEDIUM PLATE",
                "source_width_px":1200,
                "display_width_percent":70,
                "byte_budget":200000,
            },
            {
                "key":"plate-b",
                "route":"SMALL PLATE",
                "source_width_px":1200,
                "display_width_percent":60,
                "byte_budget":200000,
            },
            {
                "key":"live",
                "route":"SIMPLIFY LIVE",
            },
        ],
    }

    profile_path=tmp_path/"profile.json"
    profile_path.write_text(
        json.dumps(profile),
        encoding="utf-8",
    )

    run=tmp_path/"run"
    plates=run/"plates"
    plates.mkdir(parents=True)

    Image.new(
        "RGB",
        (1200,500),
        (244,242,235),
    ).save(plates/"plate-a.png")

    Image.new(
        "RGB",
        (1200,600),
        (239,238,231),
    ).save(plates/"plate-b.png")

    return profile_path,run


def test_batch_requires_explicit_components(tmp_path):
    profile,run=make_fixture(tmp_path)

    with pytest.raises(
        ValueError,
        match="At least one explicit component",
    ):
        run_batch_optimization_lab(
            profile_path=profile,
            run_dir=run,
            component_keys=[],
            output_dir=tmp_path/"batch",
            device_keys=("kindle-11",),
        )


def test_batch_rejects_duplicate_component_keys(tmp_path):
    profile,run=make_fixture(tmp_path)

    with pytest.raises(
        ValueError,
        match="must be unique",
    ):
        run_batch_optimization_lab(
            profile_path=profile,
            run_dir=run,
            component_keys=[
                "plate-a",
                "plate-a",
            ],
            output_dir=tmp_path/"batch",
            device_keys=("kindle-11",),
        )


def test_batch_rejects_live_component(tmp_path):
    profile,run=make_fixture(tmp_path)

    with pytest.raises(
        ValueError,
        match="not a plate route",
    ):
        run_batch_optimization_lab(
            profile_path=profile,
            run_dir=run,
            component_keys=["live"],
            output_dir=tmp_path/"batch",
            device_keys=("kindle-11",),
        )


def test_batch_produces_one_review_surface(tmp_path):
    profile,run=make_fixture(tmp_path)

    result=run_batch_optimization_lab(
        profile_path=profile,
        run_dir=run,
        component_keys=[
            "plate-a",
            "plate-b",
        ],
        output_dir=tmp_path/"batch",
        device_keys=("kindle-11",),
    )

    assert result["summary"]["component_count"] == 2

    assert (
        tmp_path
        /"batch"
        /"BATCH_REPORT.json"
    ).is_file()

    review=(
        tmp_path
        /"batch"
        /"BATCH_REVIEW.html"
    )

    assert review.is_file()

    text=review.read_text(
        encoding="utf-8"
    )

    assert "plate-a/baseline.png" in text
    assert "plate-a/palette-256.png" in text
    assert "plate-b/baseline.png" in text
    assert "plate-b/palette-256.png" in text


def test_batch_never_auto_promotes(tmp_path):
    profile,run=make_fixture(tmp_path)

    result=run_batch_optimization_lab(
        profile_path=profile,
        run_dir=run,
        component_keys=["plate-a"],
        output_dir=tmp_path/"batch",
        device_keys=("kindle-11",),
    )

    assert (
        result["policy"]["automatic_application"]
        is False
    )

    assert (
        result["policy"]["automatic_promotion"]
        is False
    )

    assert (
        result["components"][0][
            "review_status"
        ]
        == "OPEN"
    )
