from __future__ import annotations

from mfl_adapter.optimization_policy import (
    GRAPHIC_REVIEW_ZONE,
    PALETTE_256_SPARSE_EDITORIAL,
    PALETTE_256_STRUCTURED_EDITORIAL_FIELD,
    assess_plate_candidate,
    get_optimization_method,
)


def lab_report():
    return {
        "component":{
            "key":"jules-motion",
            "route":"SMALL PLATE",
        },
        "candidates":[
            {
                "name":"baseline",
                "width_px":1800,
                "height_px":2198,
                "bytes":216477,
                "device_status":"RESERVE MET",
                "byte_status":"NEAR BUDGET",
            },
            {
                "name":"palette-256",
                "width_px":1800,
                "height_px":2198,
                "bytes":83492,
                "device_status":"RESERVE MET",
                "byte_status":"WITHIN BUDGET",
            },
        ],
    }


def test_palette_method_is_admitted_but_never_automatic():
    method=get_optimization_method(
        PALETTE_256_SPARSE_EDITORIAL
    )

    assert method.method_status == "ADMITTED METHOD"
    assert method.automatic_application is False
    assert method.automatic_promotion is False


def test_graphic_review_zone_includes_typography():
    joined=" ".join(
        GRAPHIC_REVIEW_ZONE["includes"]
    ).lower()

    assert "font size" in joined
    assert "legibility" in joined
    assert "collisions" in joined


def test_graphic_review_zone_excludes_whole_page_aesthetics():
    joined=" ".join(
        GRAPHIC_REVIEW_ZONE[
            "excluded_from_component_probe_judgment"
        ]
    ).lower()

    assert "whitespace" in joined
    assert "whole-chapter" in joined
    assert "final retail composition" in joined


def test_local_and_kindle_pass_make_palette_candidate_eligible():
    result=assess_plate_candidate(
        lab_report(),
        candidate_name="palette-256",
        local_graphic="PASS",
        kindle_graphic="PASS",
        whole_page="NOT_EVALUATED",
    )

    assert (
        result["disposition"]
        == "ELIGIBLE_FOR_PLATE_ADMISSION"
    )

    assert result["automatic_promotion"] is False

    assert (
        result["human_review"][
            "whole_page_composition"
        ]
        == "NOT_EVALUATED"
    )


def test_whole_page_not_evaluated_does_not_block_plate_admission():
    result=assess_plate_candidate(
        lab_report(),
        candidate_name="palette-256",
        local_graphic="PASS",
        kindle_graphic="PASS",
    )

    assert (
        result["disposition"]
        == "ELIGIBLE_FOR_PLATE_ADMISSION"
    )


def test_graphic_failure_rejects_candidate():
    result=assess_plate_candidate(
        lab_report(),
        candidate_name="palette-256",
        local_graphic="PASS",
        kindle_graphic="FAIL",
    )

    assert result["disposition"] == "REJECT"


def test_candidate_must_actually_reduce_bytes():
    report=lab_report()

    report["candidates"][1]["bytes"]=300000

    result=assess_plate_candidate(
        report,
        candidate_name="palette-256",
        local_graphic="PASS",
        kindle_graphic="PASS",
    )

    assert result["automatic_checks"]["smaller_file"] is False
    assert result["disposition"] == "REJECT"
def test_palette_candidate_keeps_sparse_method_by_default():
    result=assess_plate_candidate(
        lab_report(),
        candidate_name="palette-256",
        local_graphic="PASS",
        kindle_graphic="PASS",
    )

    assert (
        result["method"]["method_id"]
        == PALETTE_256_SPARSE_EDITORIAL
    )

    assert (
        result["method"]["plate_class"]
        == "SPARSE EDITORIAL PLATE"
    )


def test_palette_candidate_can_use_structured_editorial_field_method():
    result=assess_plate_candidate(
        lab_report(),
        candidate_name="palette-256",
        method_id=PALETTE_256_STRUCTURED_EDITORIAL_FIELD,
        local_graphic="PASS",
        kindle_graphic="PASS",
    )

    assert (
        result["method"]["method_id"]
        == PALETTE_256_STRUCTURED_EDITORIAL_FIELD
    )

    assert (
        result["method"]["plate_class"]
        == "STRUCTURED EDITORIAL FIELD"
    )

    assert (
        result["disposition"]
        == "ELIGIBLE_FOR_PLATE_ADMISSION"
    )


def test_structured_palette_method_rejects_non_palette_candidate():
    report=lab_report()

    report["candidates"].append({
        "name":"other",
        "width_px":1800,
        "height_px":2198,
        "bytes":80000,
        "device_status":"RESERVE MET",
        "byte_status":"WITHIN BUDGET",
    })

    import pytest

    with pytest.raises(
        ValueError,
        match="requires candidate 'palette-256'",
    ):
        assess_plate_candidate(
            report,
            candidate_name="other",
            method_id=PALETTE_256_STRUCTURED_EDITORIAL_FIELD,
            local_graphic="PASS",
            kindle_graphic="PASS",
        )
