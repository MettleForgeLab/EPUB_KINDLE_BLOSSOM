from __future__ import annotations

import json

from PIL import Image
import pytest

from mfl_adapter.optimization_lab import (
    run_optimization_lab,
)


def profile():
    return {
        "components":[
            {
                "key":"plate",
                "route":"SMALL PLATE",
                "source_width_px":1800,
                "display_width_percent":62,
                "byte_budget":220000,
            },
            {
                "key":"live",
                "route":"SIMPLIFY LIVE",
            },
        ]
    }


def make_run(tmp_path):
    run=tmp_path/"run"
    plates=run/"plates"
    plates.mkdir(parents=True)

    image=Image.new(
        "RGB",
        (1800,1000),
        (240,240,240),
    )

    image.save(plates/"plate.png")

    return run


def make_profile(tmp_path):
    path=tmp_path/"profile.json"
    path.write_text(
        json.dumps(profile()),
        encoding="utf-8",
    )
    return path


def test_lab_generates_review_candidates(tmp_path):
    report=run_optimization_lab(
        profile_path=make_profile(tmp_path),
        run_dir=make_run(tmp_path),
        component_key="plate",
        output_dir=tmp_path/"lab",
        device_keys=("scribe-3",),
    )

    assert len(report["candidates"]) == 5
    assert (tmp_path/"lab"/"OPTIMIZATION_REPORT.json").is_file()
    assert (tmp_path/"lab"/"REVIEW.html").is_file()


def test_lab_never_auto_promotes(tmp_path):
    report=run_optimization_lab(
        profile_path=make_profile(tmp_path),
        run_dir=make_run(tmp_path),
        component_key="plate",
        output_dir=tmp_path/"lab",
        device_keys=("scribe-3",),
    )

    assert report["policy"]["automatic_promotion"] is False

    for item in report["candidates"][1:]:
        assert item["promotion_status"] == "REVIEW ONLY"


def test_reserve_candidate_uses_exact_required_width(tmp_path):
    report=run_optimization_lab(
        profile_path=make_profile(tmp_path),
        run_dir=make_run(tmp_path),
        component_key="plate",
        output_dir=tmp_path/"lab",
        device_keys=("scribe-3",),
    )

    reserve=next(
        item
        for item in report["candidates"]
        if item["name"] == "reserve-width-rgb"
    )

    assert (
        reserve["width_px"]
        == report["policy"]["reserve_width_px"]
    )


def test_grayscale_is_explicitly_simulation(tmp_path):
    report=run_optimization_lab(
        profile_path=make_profile(tmp_path),
        run_dir=make_run(tmp_path),
        component_key="plate",
        output_dir=tmp_path/"lab",
        device_keys=("scribe-3",),
    )

    gray=next(
        item
        for item in report["candidates"]
        if item["name"] == "grayscale-simulation"
    )

    assert "simulation" in gray["purpose"].lower()
    assert gray["promotion_status"] == "REVIEW ONLY"


def test_lab_rejects_live_component(tmp_path):
    with pytest.raises(
        ValueError,
        match="not a plate route",
    ):
        run_optimization_lab(
            profile_path=make_profile(tmp_path),
            run_dir=make_run(tmp_path),
            component_key="live",
            output_dir=tmp_path/"lab",
            device_keys=("scribe-3",),
        )


def test_lab_refuses_existing_output_directory(tmp_path):
    output=tmp_path/"lab"
    output.mkdir()

    with pytest.raises(FileExistsError):
        run_optimization_lab(
            profile_path=make_profile(tmp_path),
            run_dir=make_run(tmp_path),
            component_key="plate",
            output_dir=output,
            device_keys=("scribe-3",),
        )
