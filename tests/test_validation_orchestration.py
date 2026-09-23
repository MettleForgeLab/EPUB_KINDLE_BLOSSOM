from __future__ import annotations

from pathlib import Path

from mfl_adapter.validation import run_validation


def _tool_files(tmp_path):
    java=tmp_path/"java.exe"
    epubcheck=tmp_path/"epubcheck.jar"
    ace=tmp_path/"ace.cmd"

    for path in (java,epubcheck,ace):
        path.write_bytes(b"x")

    return java,epubcheck,ace


def test_unified_validation_pass_keeps_human_separate(
    tmp_path,
    monkeypatch,
):
    epub=tmp_path/"book.epub"
    epub.write_bytes(b"book")

    java,epubcheck,ace=_tool_files(tmp_path)

    monkeypatch.setattr(
        "mfl_adapter.validation.read_zip",
        lambda path: {"mimetype":b"application/epub+zip"},
    )

    monkeypatch.setattr(
        "mfl_adapter.validation.package_report",
        lambda members: {"status":"passed"},
    )

    monkeypatch.setattr(
        "mfl_adapter.validation.run_epubcheck",
        lambda *args,**kwargs:{
            "execution":"PASS",
            "conformance":"PASS",
            "exit_code":0,
        },
    )

    monkeypatch.setattr(
        "mfl_adapter.validation.run_ace",
        lambda *args,**kwargs:{
            "execution":"PASS",
            "automated_accessibility":"PASS",
            "exit_code":0,
        },
    )

    report=run_validation(
        epub,
        project_root=tmp_path,
        output_dir=tmp_path/"validation",
        java=java,
        epubcheck=epubcheck,
        ace=ace,
    )

    assert report["overall_automated_status"] == "PASS"
    assert report["kindle_previewer"]["status"] == "NOT RUN"
    assert report["human_acceptance"]["status"] == "NOT RUN"
    assert report["certification"]["status"] == "NOT CLAIMED"


def test_unified_validation_preserves_ace_findings(
    tmp_path,
    monkeypatch,
):
    epub=tmp_path/"book.epub"
    epub.write_bytes(b"book")

    java,epubcheck,ace=_tool_files(tmp_path)

    monkeypatch.setattr(
        "mfl_adapter.validation.read_zip",
        lambda path: {"mimetype":b"application/epub+zip"},
    )

    monkeypatch.setattr(
        "mfl_adapter.validation.package_report",
        lambda members: {"status":"passed"},
    )

    monkeypatch.setattr(
        "mfl_adapter.validation.run_epubcheck",
        lambda *args,**kwargs:{
            "execution":"PASS",
            "conformance":"PASS",
            "exit_code":0,
        },
    )

    monkeypatch.setattr(
        "mfl_adapter.validation.run_ace",
        lambda *args,**kwargs:{
            "execution":"PASS",
            "automated_accessibility":"FINDINGS",
            "exit_code":2,
        },
    )

    report=run_validation(
        epub,
        project_root=tmp_path,
        output_dir=tmp_path/"validation",
        java=java,
        epubcheck=epubcheck,
        ace=ace,
    )

    assert report["overall_automated_status"] == "FINDINGS"
    assert report["human_acceptance"]["status"] == "NOT RUN"
