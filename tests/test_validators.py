from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from mfl_adapter.validators.epubcheck import run_epubcheck
from mfl_adapter.validators.ace import run_ace


def fake_file(path: Path):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(b"x")


def test_epubcheck_zero_exit_means_conformance_pass(
    tmp_path,
    monkeypatch,
):
    epub=tmp_path/"book.epub"
    java=tmp_path/"java.exe"
    jar=tmp_path/"epubcheck.jar"

    for path in (epub,java,jar):
        fake_file(path)

    def fake_run(command,**kwargs):
        json_path=Path(
            command[command.index("--json")+1]
        )
        json_path.write_text(
            json.dumps({"messages":[]}),
            encoding="utf-8",
        )

        return SimpleNamespace(
            returncode=0,
            stdout="clean",
            stderr="",
        )

    monkeypatch.setattr(
        "mfl_adapter.validators.epubcheck.subprocess.run",
        fake_run,
    )

    result=run_epubcheck(
        epub,
        java=java,
        jar=jar,
        report_dir=tmp_path/"report",
    )

    assert result["execution"] == "PASS"
    assert result["conformance"] == "PASS"
    assert result["exit_code"] == 0


def test_ace_exit_two_is_findings_not_tool_failure(
    tmp_path,
    monkeypatch,
):
    epub=tmp_path/"book.epub"
    ace=tmp_path/"ace.cmd"

    for path in (epub,ace):
        fake_file(path)

    report_dir=tmp_path/"report"

    report={
        "a11y-metadata":{
            "missing":["dcterms:conformsTo"],
            "empty":[],
            "present":["schema:accessMode"],
        },
        "assertions":[
            {
                "earl:test":{
                    "dct:title":"example-rule",
                    "earl:impact":"moderate",
                },
                "earl:result":{
                    "earl:outcome":"fail",
                    "dct:description":"example finding",
                },
            }
        ],
    }

    def fake_run(command,**kwargs):
        report_dir.mkdir(parents=True,exist_ok=True)

        (report_dir/"report.json").write_text(
            json.dumps(report),
            encoding="utf-8",
        )

        (report_dir/"report.html").write_text(
            "<html></html>",
            encoding="utf-8",
        )

        return SimpleNamespace(
            returncode=2,
            stdout="findings",
            stderr="",
        )

    monkeypatch.setattr(
        "mfl_adapter.validators.ace.subprocess.run",
        fake_run,
    )

    result=run_ace(
        epub,
        ace=ace,
        report_dir=report_dir,
    )

    assert result["execution"] == "PASS"
    assert result["automated_accessibility"] == "FINDINGS"
    assert result["exit_code"] == 2
    assert len(result["failed_assertions"]) == 1


def test_ace_zero_exit_is_automated_pass(
    tmp_path,
    monkeypatch,
):
    epub=tmp_path/"book.epub"
    ace=tmp_path/"ace.cmd"

    for path in (epub,ace):
        fake_file(path)

    report_dir=tmp_path/"report"

    def fake_run(command,**kwargs):
        report_dir.mkdir(parents=True,exist_ok=True)

        (report_dir/"report.json").write_text(
            json.dumps({
                "a11y-metadata":{
                    "missing":[],
                    "empty":[],
                    "present":[],
                }
            }),
            encoding="utf-8",
        )

        (report_dir/"report.html").write_text(
            "<html></html>",
            encoding="utf-8",
        )

        return SimpleNamespace(
            returncode=0,
            stdout="clean",
            stderr="",
        )

    monkeypatch.setattr(
        "mfl_adapter.validators.ace.subprocess.run",
        fake_run,
    )

    result=run_ace(
        epub,
        ace=ace,
        report_dir=report_dir,
    )

    assert result["execution"] == "PASS"
    assert result["automated_accessibility"] == "PASS"
    assert result["failed_assertions"] == []

def test_windows_ace_cmd_uses_python_shell_escaping():
    from pathlib import Path

    from mfl_adapter.validators.ace import _ace_launch

    ace=Path(
        r"C:\MFL Kindle Visual Adapter\tools\ace\1.4.6\ace.cmd"
    )

    command,use_shell=_ace_launch(
        ace,
        [
            "--outdir",
            r"C:\MFL Kindle Visual Adapter\runs\report",
            r"C:\MFL Kindle Visual Adapter\book.epub",
        ],
        windows=True,
    )

    assert use_shell is True
    assert isinstance(command,str)
    assert "ace.cmd" in command
    assert "MFL Kindle Visual Adapter" in command
    assert "--outdir" in command
