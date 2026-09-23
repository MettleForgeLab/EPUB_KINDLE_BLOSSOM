"""Normalized MFL validation evidence.

The report distinguishes implementation evidence, automated validation,
Kindle conversion evidence, and human acceptance. Absence of evidence is
recorded as NOT RUN rather than silently promoted to PASS.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .core import digest
from .tooling import discover_optional_tools


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
    epub = Path(epub).resolve()

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
            note="Conformance validator; not yet executed."
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
            note="Porter acceptance remains separate and explicit.",
        ),
        discovered_tools=discover_optional_tools(project_root),
    )


def write_validation_report(
    report: ValidationReport,
    destination: str | Path,
) -> Path:
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    destination.write_text(
        json.dumps(
            report.to_dict(),
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    return destination
