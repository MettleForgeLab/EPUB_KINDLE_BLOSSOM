"""EPUBCheck external validator adapter."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any


def run_epubcheck(
    epub: str | Path,
    *,
    java: str | Path,
    jar: str | Path,
    report_dir: str | Path,
) -> dict[str, Any]:
    epub=Path(epub).resolve()
    java=Path(java).resolve()
    jar=Path(jar).resolve()
    report_dir=Path(report_dir).resolve()

    if not epub.is_file():
        raise FileNotFoundError(epub)

    if not java.is_file():
        raise FileNotFoundError(java)

    if not jar.is_file():
        raise FileNotFoundError(jar)

    report_dir.mkdir(parents=True,exist_ok=True)

    json_report=report_dir/"epubcheck-report.json"

    command=[
        str(java),
        "-jar",
        str(jar),
        str(epub),
        "--json",
        str(json_report),
    ]

    completed=subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    parsed=None

    if json_report.is_file():
        parsed=json.loads(
            json_report.read_text(encoding="utf-8")
        )

    if completed.returncode == 0:
        execution="PASS"
        conformance="PASS"

    elif json_report.is_file():
        execution="PASS"
        conformance="FAIL"

    else:
        execution="TOOL ERROR"
        conformance="NOT DETERMINED"

    return {
        "tool":"EPUBCheck",
        "execution":execution,
        "conformance":conformance,
        "exit_code":completed.returncode,
        "command":command,
        "stdout":completed.stdout,
        "stderr":completed.stderr,
        "report_path":(
            str(json_report)
            if json_report.is_file()
            else None
        ),
        "report":parsed,
    }
