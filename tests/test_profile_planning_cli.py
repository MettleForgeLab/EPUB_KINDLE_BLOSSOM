from __future__ import annotations

import json
from types import SimpleNamespace

from mfl_adapter.__main__ import plan_profile_cli


def test_plan_profile_cli(tmp_path,capsys):
    profile={
        "profile_id":"cli-test",
        "profile_version":"1",
        "mode":"test",
        "components":[
            {
                "key":"plate",
                "route":"MEDIUM PLATE",
                "source_width_px":2000,
                "display_width_percent":72,
                "byte_budget":250000,
            }
        ],
    }

    profile_path=tmp_path/"profile.json"
    profile_path.write_text(
        json.dumps(profile),
        encoding="utf-8",
    )

    output=tmp_path/"plan.json"

    args=SimpleNamespace(
        profile=str(profile_path),
        run=None,
        devices=["scribe-3"],
        reserve_ratio=1.25,
        overbuilt_headroom=1.50,
        out=str(output),
    )

    assert plan_profile_cli(args) == 0

    stdout=json.loads(
        capsys.readouterr().out
    )

    assert stdout["summary"]["plate_count"] == 1
    assert stdout["components"][0]["planning_status"] == "RESERVE MET"
    assert output.is_file()
