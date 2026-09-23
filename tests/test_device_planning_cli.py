from __future__ import annotations

import json
from types import SimpleNamespace

from mfl_adapter.__main__ import plan_plate_cli


def test_plan_plate_cli_emits_and_writes_json(
    tmp_path,
    capsys,
):
    destination=tmp_path/"plan.json"

    args=SimpleNamespace(
        width=2000,
        height=1500,
        display_fraction=0.72,
        devices=[
            "paperwhite-6",
            "colorsoft",
            "scribe-3",
        ],
        reserve_ratio=1.25,
        out=str(destination),
    )

    assert plan_plate_cli(args) == 0

    stdout=json.loads(
        capsys.readouterr().out
    )

    saved=json.loads(
        destination.read_text(encoding="utf-8")
    )

    assert stdout == saved
    assert stdout["worst_status"] == "RESERVE MET"
    assert (
        stdout["minimum_source_width_for_all_devices_px"]
        == 1788
    )


def test_plan_plate_cli_reports_underresolved(
    capsys,
):
    args=SimpleNamespace(
        width=800,
        height=600,
        display_fraction=0.90,
        devices=["scribe-3"],
        reserve_ratio=1.25,
        out=None,
    )

    assert plan_plate_cli(args) == 0

    result=json.loads(
        capsys.readouterr().out
    )

    assert result["worst_status"] == "UNDER-RESOLVED"
