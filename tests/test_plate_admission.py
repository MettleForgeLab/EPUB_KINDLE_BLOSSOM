from __future__ import annotations

import json

from PIL import Image
import pytest

from mfl_adapter.core import digest
from mfl_adapter.plate_admission import (
    apply_plate_admissions,
    create_plate_admission,
    verify_admission_packet,
)


def png(path,color):
    Image.new(
        "RGB",
        (120,80),
        color,
    ).save(path)

    return path


def profile_file(tmp_path):
    profile={
        "profile_id":"admission-test",
        "profile_version":"2",
        "components":[
            {
                "key":"plate",
                "route":"SMALL PLATE",
            }
        ],
    }

    path=tmp_path/"profile.json"
    path.write_text(
        json.dumps(profile),
        encoding="utf-8",
    )

    return path


def review_file(
    tmp_path,
    baseline,
    candidate,
):
    review={
        "schema":"mfl.plate-optimization-review/1",
        "component":{
            "key":"plate",
            "route":"SMALL PLATE",
        },
        "candidate":"palette-256",
        "method":{
            "method_id":"palette-256-sparse-editorial",
            "method_status":"ADMITTED METHOD",
            "automatic_promotion":False,
            "preserves_dimensions":True,
        },
        "human_review":{
            "local_graphic":"PASS",
            "kindle_graphic":"PASS",
            "whole_page_composition":"NOT_EVALUATED",
        },
        "baseline":{
            "width_px":120,
            "height_px":80,
            "bytes":baseline.stat().st_size,
        },
        "candidate_evidence":{
            "width_px":120,
            "height_px":80,
            "bytes":candidate.stat().st_size,
        },
        "disposition":"ELIGIBLE_FOR_PLATE_ADMISSION",
        "automatic_promotion":False,
        "publication_replacement_performed":False,
    }

    path=tmp_path/"review.json"
    path.write_text(
        json.dumps(review),
        encoding="utf-8",
    )

    return path


def assets(tmp_path):
    baseline=png(
        tmp_path/"baseline.png",
        (255,255,255),
    )

    candidate=png(
        tmp_path/"candidate.png",
        (0,0,0),
    )

    # Ensure candidate is smaller for admission-policy purposes.
    if candidate.stat().st_size >= baseline.stat().st_size:
        candidate.write_bytes(
            b"\x89PNG\r\n\x1a\n"
        )
        pytest.skip(
            "Synthetic PNG sizes are unsuitable on this Pillow runtime."
        )

    return baseline,candidate


def test_admission_requires_explicit_admit(tmp_path):
    baseline,candidate=assets(tmp_path)
    profile=profile_file(tmp_path)
    review=review_file(
        tmp_path,
        baseline,
        candidate,
    )

    with pytest.raises(
        ValueError,
        match="exactly 'ADMIT'",
    ):
        create_plate_admission(
            review_path=review,
            candidate_path=candidate,
            baseline_path=baseline,
            profile_path=profile,
            output_dir=tmp_path/"packet",
            authorized_by="Reviewer",
            authorization="YES",
        )


def test_admission_packet_is_self_contained_and_verifiable(
    tmp_path,
):
    baseline,candidate=assets(tmp_path)
    profile=profile_file(tmp_path)
    review=review_file(
        tmp_path,
        baseline,
        candidate,
    )

    create_plate_admission(
        review_path=review,
        candidate_path=candidate,
        baseline_path=baseline,
        profile_path=profile,
        output_dir=tmp_path/"packet",
        authorized_by="Reviewer",
        authorization="ADMIT",
    )

    verified=verify_admission_packet(
        tmp_path/"packet"/"PLATE_ADMISSION.json",
        profile_path=profile,
    )

    assert verified["record"]["component"]["key"] == "plate"
    assert verified["candidate_path"].is_file()
    assert verified["baseline_path"].is_file()
    assert verified["review_path"].is_file()


def test_profile_drift_stops_admission_verification(tmp_path):
    baseline,candidate=assets(tmp_path)
    profile=profile_file(tmp_path)
    review=review_file(
        tmp_path,
        baseline,
        candidate,
    )

    create_plate_admission(
        review_path=review,
        candidate_path=candidate,
        baseline_path=baseline,
        profile_path=profile,
        output_dir=tmp_path/"packet",
        authorized_by="Reviewer",
        authorization="ADMIT",
    )

    profile.write_text(
        profile.read_text(encoding="utf-8")+" ",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="profile SHA-256",
    ):
        verify_admission_packet(
            tmp_path/"packet"/"PLATE_ADMISSION.json",
            profile_path=profile,
        )


def test_apply_admission_replaces_plate_and_annotates(
    tmp_path,
):
    baseline,candidate=assets(tmp_path)
    profile=profile_file(tmp_path)
    review=review_file(
        tmp_path,
        baseline,
        candidate,
    )

    create_plate_admission(
        review_path=review,
        candidate_path=candidate,
        baseline_path=baseline,
        profile_path=profile,
        output_dir=tmp_path/"packet",
        authorized_by="Reviewer",
        authorization="ADMIT",
    )

    run=tmp_path/"run"
    plates=run/"plates"
    plates.mkdir(parents=True)

    rendered_plate=plates/"plate.png"
    rendered_plate.write_bytes(
        baseline.read_bytes()
    )

    rendering={
        "plates":[
            {
                "key":"plate",
                "human_visual_acceptance":"open",
                "kindle_rendering":"not tested",
            }
        ]
    }

    result=apply_plate_admissions(
        [
            tmp_path
            /"packet"
            /"PLATE_ADMISSION.json"
        ],
        profile_path=profile,
        run_dir=run,
        rendering=rendering,
    )

    assert result["admission_count"] == 1
    assert (
        rendered_plate.read_bytes()
        == candidate.read_bytes()
    )

    admitted=rendering["plates"][0]["admission"]

    assert admitted["status"] == "ADMITTED"
    assert admitted["authorized_by"] == "Reviewer"


def test_baseline_drift_stops_admission_application(
    tmp_path,
):
    baseline,candidate=assets(tmp_path)
    profile=profile_file(tmp_path)
    review=review_file(
        tmp_path,
        baseline,
        candidate,
    )

    create_plate_admission(
        review_path=review,
        candidate_path=candidate,
        baseline_path=baseline,
        profile_path=profile,
        output_dir=tmp_path/"packet",
        authorized_by="Reviewer",
        authorization="ADMIT",
    )

    run=tmp_path/"run"
    plates=run/"plates"
    plates.mkdir(parents=True)

    png(
        plates/"plate.png",
        (128,128,128),
    )

    rendering={
        "plates":[
            {
                "key":"plate",
            }
        ]
    }

    with pytest.raises(
        ValueError,
        match="rendered baseline SHA-256",
    ):
        apply_plate_admissions(
            [
                tmp_path
                /"packet"
                /"PLATE_ADMISSION.json"
            ],
            profile_path=profile,
            run_dir=run,
            rendering=rendering,
        )

def test_apply_admission_updates_active_render_metrics(
    tmp_path,
):
    baseline,candidate=assets(tmp_path)
    profile=profile_file(tmp_path)
    review=review_file(
        tmp_path,
        baseline,
        candidate,
    )

    create_plate_admission(
        review_path=review,
        candidate_path=candidate,
        baseline_path=baseline,
        profile_path=profile,
        output_dir=tmp_path/"packet",
        authorized_by="Reviewer",
        authorization="ADMIT",
    )

    run=tmp_path/"run"
    plates=run/"plates"
    plates.mkdir(parents=True)

    rendered_plate=plates/"plate.png"
    rendered_plate.write_bytes(
        baseline.read_bytes()
    )

    rendering={
        "plates":[
            {
                "key":"plate",
                "budget_bytes":1000000,
                "optimization":{
                    "selected":"lossless RGB",
                    "selected_bytes":baseline.stat().st_size,
                    "selected_sha256":digest(
                        baseline.read_bytes()
                    ),
                },
                "human_visual_acceptance":"open",
                "kindle_rendering":"not tested",
            }
        ]
    }

    apply_plate_admissions(
        [
            tmp_path
            /"packet"
            /"PLATE_ADMISSION.json"
        ],
        profile_path=profile,
        run_dir=run,
        rendering=rendering,
    )

    item=rendering["plates"][0]

    assert (
        item["baseline_render_optimization"]["selected"]
        == "lossless RGB"
    )

    assert (
        item["optimization"]["selected"]
        == "admitted palette-256"
    )

    assert (
        item["optimization"]["selected_sha256"]
        == digest(candidate.read_bytes())
    )

    assert (
        item["optimization"]["selected_bytes"]
        == candidate.stat().st_size
    )

    assert item["within_budget"] is True
    assert item["admission"]["status"] == "ADMITTED"
