"""Ace by DAISY external validator adapter."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any


ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def _clean(text: str) -> str:
    return ANSI.sub("", text or "")


def _failed_assertions(obj) -> list[dict[str, Any]]:
    failures = []

    def walk(value):
        if isinstance(value, dict):
            test = value.get("earl:test")
            result = value.get("earl:result")

            if isinstance(test, dict) and isinstance(result, dict):
                if result.get("earl:outcome") == "fail":
                    failures.append({
                        "rule": test.get("dct:title"),
                        "impact": test.get("earl:impact"),
                        "description": result.get("dct:description"),
                    })

            for child in value.values():
                walk(child)

        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(obj)
    return failures


def _ace_launch(
    ace: Path,
    arguments: list[str],
    *,
    windows: bool | None = None,
):
    """Return command plus shell policy for the installed Ace launcher."""
    base = [str(ace), *arguments]

    if windows is None:
        windows = os.name == "nt"

    if windows and ace.suffix.lower() in (".cmd", ".bat"):
        # npm exposes Ace as a Windows command wrapper.
        # Let Python construct Windows quoting once and let COMSPEC
        # execute the wrapper.
        return subprocess.list2cmdline(base), True

    return base, False


def run_ace(
    epub: str | Path,
    *,
    ace: str | Path,
    report_dir: str | Path,
) -> dict[str, Any]:
    epub = Path(epub).resolve()
    ace = Path(ace).resolve()
    report_dir = Path(report_dir).resolve()

    if not epub.is_file():
        raise FileNotFoundError(epub)

    if not ace.is_file():
        raise FileNotFoundError(ace)

    report_dir.mkdir(parents=True, exist_ok=True)

    arguments = [
        "--outdir",
        str(report_dir),
        "--force",
        "--exiterror2",
        str(epub),
    ]

    command, use_shell = _ace_launch(ace, arguments)

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        shell=use_shell,
    )

    json_report = report_dir / "report.json"
    html_report = report_dir / "report.html"

    parsed = None

    if json_report.is_file():
        parsed = json.loads(
            json_report.read_text(encoding="utf-8")
        )

    if completed.returncode in (0, 2):
        execution = "PASS"
    else:
        execution = "TOOL ERROR"

    if execution != "PASS":
        automated = "NOT DETERMINED"
    elif completed.returncode == 2:
        automated = "FINDINGS"
    else:
        automated = "PASS"

    failures = (
        _failed_assertions(parsed)
        if parsed is not None
        else []
    )

    metadata = (
        parsed.get("a11y-metadata", {})
        if isinstance(parsed, dict)
        else {}
    )

    return {
        "tool": "Ace by DAISY",
        "execution": execution,
        "automated_accessibility": automated,
        "exit_code": completed.returncode,
        "command": command,
        "shell": use_shell,
        "stdout": _clean(completed.stdout),
        "stderr": _clean(completed.stderr),
        "json_report_path": (
            str(json_report)
            if json_report.is_file()
            else None
        ),
        "html_report_path": (
            str(html_report)
            if html_report.is_file()
            else None
        ),
        "failed_assertions": failures,
        "accessibility_metadata": {
            "missing": metadata.get("missing", []),
            "empty": metadata.get("empty", []),
            "present": metadata.get("present", []),
        },
    }
