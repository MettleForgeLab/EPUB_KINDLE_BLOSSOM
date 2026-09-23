"""Unified MFL validation evidence.

Automated validation, Kindle conversion, and human acceptance remain
explicitly separate kinds of evidence.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any

from .core import digest, package_report, read_zip
from .validators.ace import run_ace
from .validators.epubcheck import run_epubcheck


@dataclass
class ValidationStage:
    status: str = "NOT RUN"
    tool: str | None = None
    version: str | None = None
    exit_code: int | None = None
    report_path: str | None = None
    findings: dict[str, Any] = field(default_factory=dict)
    note: str | None = None


@dataclass
class ValidationReport:
    schema: str
    generated_utc: str
    epub_path: str
    epub_sha256: str
    internal_verifier: ValidationStage
    epubcheck: ValidationStage
    ace: ValidationStage
    kindle_previewer: ValidationStage
    human_acceptance: ValidationStage
    discovered_tools: dict[str, Any]

    def to_dict(self) -> dict:
        return asdict(self)


def new_validation_report(
    epub: str | Path,
    project_root: str | Path,
) -> ValidationReport:
    epub=Path(epub).resolve()

    if not epub.is_file():
        raise FileNotFoundError(epub)

    return ValidationReport(
        schema="mfl.validation-report/1",
        generated_utc=datetime.now(timezone.utc).isoformat(),
        epub_path=str(epub),
        epub_sha256=digest(epub.read_bytes()),
        internal_verifier=ValidationStage(),
        epubcheck=ValidationStage(
            tool="EPUBCheck",
            note="Conformance validator; not yet executed.",
        ),
        ace=ValidationStage(
            tool="Ace by DAISY",
            note=(
                "Automated accessibility checker; findings require "
                "human interpretation."
            ),
        ),
        kindle_previewer=ValidationStage(
            tool="Kindle Previewer",
            note=(
                "Amazon conversion/render evidence remains separate "
                "from EPUB conformance."
            ),
        ),
        human_acceptance=ValidationStage(
            tool="Human review",
            note="Human acceptance remains separate and explicit.",
        ),
        discovered_tools={},
    )


def write_validation_report(
    report: ValidationReport,
    destination: str | Path,
) -> Path:
    destination=Path(destination)
    destination.parent.mkdir(parents=True,exist_ok=True)

    destination.write_text(
        json.dumps(
            report.to_dict(),
            ensure_ascii=False,
            indent=2,
        )+"\n",
        encoding="utf-8",
    )

    return destination


def _read_json_if_present(path: Path) -> dict | None:
    if not path.is_file():
        return None

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def _nearest_install_record(path: Path) -> dict | None:
    current=path.parent

    for _ in range(6):
        candidate=current/"MFL_INSTALL_RECORD.json"

        if candidate.is_file():
            return _read_json_if_present(candidate)

        parent=current.parent

        if parent == current:
            break

        current=parent

    return None


def default_tool_paths(
    project_root: str | Path,
) -> dict[str, Path]:
    root=Path(project_root).resolve()

    java_name=(
        "java.exe"
        if os.name == "nt"
        else "java"
    )

    ace_name=(
        "ace.cmd"
        if os.name == "nt"
        else "ace"
    )

    return {
        "java":(
            root
            /"tools"
            /"java"
            /"temurin-21"
            /"bin"
            /java_name
        ),
        "epubcheck":(
            root
            /"tools"
            /"epubcheck"
            /"5.4.0"
            /"epubcheck.jar"
        ),
        "ace":(
            root
            /"tools"
            /"ace"
            /"1.4.6"
            /"node_modules"
            /".bin"
            /ace_name
        ),
    }


def run_validation(
    epub: str | Path,
    *,
    project_root: str | Path,
    output_dir: str | Path,
    java: str | Path | None = None,
    epubcheck: str | Path | None = None,
    ace: str | Path | None = None,
) -> dict[str, Any]:
    epub=Path(epub).resolve()
    project_root=Path(project_root).resolve()
    output_dir=Path(output_dir).resolve()

    if not epub.is_file():
        raise FileNotFoundError(epub)

    defaults=default_tool_paths(project_root)

    java=Path(java or defaults["java"]).resolve()
    epubcheck=Path(
        epubcheck or defaults["epubcheck"]
    ).resolve()
    ace=Path(ace or defaults["ace"]).resolve()

    for label,path in (
        ("Java",java),
        ("EPUBCheck",epubcheck),
        ("Ace",ace),
    ):
        if not path.is_file():
            raise FileNotFoundError(
                f"{label} executable/resource not found: {path}"
            )

    output_dir.mkdir(parents=True,exist_ok=True)

    internal=package_report(
        read_zip(epub)
    )

    epubcheck_result=run_epubcheck(
        epub,
        java=java,
        jar=epubcheck,
        report_dir=output_dir/"epubcheck",
    )

    ace_result=run_ace(
        epub,
        ace=ace,
        report_dir=output_dir/"ace",
    )

    tool_error=(
        epubcheck_result["execution"] == "TOOL ERROR"
        or ace_result["execution"] == "TOOL ERROR"
    )

    findings=(
        epubcheck_result["conformance"] == "FAIL"
        or ace_result["automated_accessibility"] == "FINDINGS"
    )

    if tool_error:
        overall="TOOL ERROR"
    elif findings:
        overall="FINDINGS"
    else:
        overall="PASS"

    report={
        "schema":"mfl.validation-report/1",
        "generated_utc":datetime.now(
            timezone.utc
        ).isoformat(),
        "overall_automated_status":overall,
        "publication":{
            "path":str(epub),
            "filename":epub.name,
            "sha256":digest(epub.read_bytes()),
            "bytes":epub.stat().st_size,
        },
        "internal_verifier":{
            "status":"PASS",
            "package":internal,
        },
        "epubcheck":epubcheck_result,
        "ace":ace_result,
        "tools":{
            "java":{
                "path":str(java),
                "install_record":_nearest_install_record(java),
            },
            "epubcheck":{
                "path":str(epubcheck),
                "install_record":_nearest_install_record(epubcheck),
            },
            "ace":{
                "path":str(ace),
                "install_record":_nearest_install_record(ace),
            },
        },
        "kindle_previewer":{
            "status":"NOT RUN",
            "note":(
                "Kindle conversion/render evidence must be "
                "recorded separately."
            ),
        },
        "human_acceptance":{
            "status":"NOT RUN",
            "note":(
                "Automated checks do not promote human "
                "visual or accessibility acceptance."
            ),
        },
        "certification":{
            "status":"NOT CLAIMED",
            "note":(
                "No accessibility certification or formal "
                "conformance claim is inferred from automated checks."
            ),
        },
    }

    report_path=output_dir/"VALIDATION_REPORT.json"

    report_path.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        )+"\n",
        encoding="utf-8",
    )

    summary=[
        "# MFL Validation Summary",
        "",
        f"**Publication:** `{epub.name}`",
        f"**SHA-256:** `{report['publication']['sha256']}`",
        f"**Automated status:** **{overall}**",
        "",
        "## Gates",
        "",
        f"- Internal package verifier: **PASS**",
        (
            "- EPUBCheck: "
            f"**{epubcheck_result['conformance']}** "
            f"(execution {epubcheck_result['execution']}, "
            f"exit {epubcheck_result['exit_code']})"
        ),
        (
            "- Ace automated accessibility: "
            f"**{ace_result['automated_accessibility']}** "
            f"(execution {ace_result['execution']}, "
            f"exit {ace_result['exit_code']})"
        ),
        "- Kindle Previewer: **NOT RUN**",
        "- Human acceptance: **NOT RUN**",
        "- Accessibility certification/conformance: **NOT CLAIMED**",
        "",
    ]

    (output_dir/"VALIDATION_SUMMARY.md").write_text(
        "\n".join(summary),
        encoding="utf-8",
    )

    return report
