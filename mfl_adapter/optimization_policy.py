"""Human-governed plate optimization policy.

An admitted optimization method may be considered for a class of plates.
No method automatically promotes a candidate into a publication.

Graphic review includes typography rendered inside the plate.
Whole-page composition remains a separate review concern.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


PALETTE_256_SPARSE_EDITORIAL = (
    "palette-256-sparse-editorial"
)

PALETTE_256_STRUCTURED_EDITORIAL_FIELD = (
    "palette-256-structured-editorial-field"
)

VALID_REVIEW_STATUSES = {
    "PASS",
    "FAIL",
    "OPEN",
    "NOT_EVALUATED",
}


@dataclass(frozen=True)
class OptimizationMethod:
    method_id: str
    label: str
    method_status: str
    plate_class: str
    automatic_application: bool
    automatic_promotion: bool
    preserves_dimensions: bool
    requires_smaller_file: bool
    requires_device_reserve: bool
    implementation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


OPTIMIZATION_METHODS = {
    PALETTE_256_SPARSE_EDITORIAL: OptimizationMethod(
        method_id=PALETTE_256_SPARSE_EDITORIAL,
        label="Full-resolution deterministic Palette-256",
        method_status="ADMITTED METHOD",
        plate_class="SPARSE EDITORIAL PLATE",
        automatic_application=False,
        automatic_promotion=False,
        preserves_dimensions=True,
        requires_smaller_file=True,
        requires_device_reserve=True,
        implementation=(
            "Deterministic 256-color indexed PNG, no dithering, "
            "at the admitted plate's full spatial resolution."
        ),
    ),

    PALETTE_256_STRUCTURED_EDITORIAL_FIELD: OptimizationMethod(
        method_id=PALETTE_256_STRUCTURED_EDITORIAL_FIELD,
        label=(
            "Full-resolution deterministic Palette-256 "
            "for structured editorial fields"
        ),
        method_status="ADMITTED METHOD",
        plate_class="STRUCTURED EDITORIAL FIELD",
        automatic_application=False,
        automatic_promotion=False,
        preserves_dimensions=True,
        requires_smaller_file=True,
        requires_device_reserve=True,
        implementation=(
            "Deterministic 256-color indexed PNG, no dithering, "
            "at the admitted plate's full spatial resolution."
        ),
    ),
}


GRAPHIC_REVIEW_ZONE = {
    "includes": [
        (
            "All typography rendered inside the plate, including "
            "font size, weight, spacing, legibility, and collisions."
        ),
        (
            "Paths, lines, nodes, jewels, arrows, endpoints, seams, "
            "and other internal relational geometry."
        ),
        (
            "Internal negative space, crop integrity, clipping, "
            "and whether labels remain attached to their intended objects."
        ),
        (
            "Color and tonal distinctions, background smoothness, "
            "banding, posterization, and other encoding-visible changes."
        ),
        (
            "Whether the plate preserves the same relational proposition "
            "and visual hierarchy as its accepted baseline."
        ),
    ],
    "excluded_from_component_probe_judgment": [
        "Surrounding Kindle page whitespace.",
        "Whole-chapter or whole-book pacing.",
        "Whether the complete page feels like the final retail composition.",
    ],
    "separate_gate": (
        "Figure/caption/link adjacency and full-page composition may be "
        "reviewed separately when the integrated publication is tested."
    ),
}


def get_optimization_method(
    method_id: str,
) -> OptimizationMethod:
    try:
        return OPTIMIZATION_METHODS[method_id]
    except KeyError as exc:
        known=", ".join(sorted(OPTIMIZATION_METHODS))
        raise KeyError(
            f"Unknown optimization method {method_id!r}. "
            f"Known methods: {known}"
        ) from exc


def method_for_candidate(
    candidate_name: str,
    method_id: str | None = None,
) -> OptimizationMethod | None:
    if method_id is not None:
        method=get_optimization_method(method_id)

        palette_methods={
            PALETTE_256_SPARSE_EDITORIAL,
            PALETTE_256_STRUCTURED_EDITORIAL_FIELD,
        }

        if (
            method.method_id in palette_methods
            and candidate_name != "palette-256"
        ):
            raise ValueError(
                f"Optimization method {method.method_id!r} "
                f"requires candidate 'palette-256', not "
                f"{candidate_name!r}."
            )

        return method

    # Backward compatibility for all existing 0.6-0.9 review records.
    if candidate_name == "palette-256":
        return get_optimization_method(
            PALETTE_256_SPARSE_EDITORIAL
        )

    return None


def _review_status(name: str, value: str) -> str:
    value=value.upper()

    if value not in VALID_REVIEW_STATUSES:
        raise ValueError(
            f"{name} must be one of: "
            + ", ".join(sorted(VALID_REVIEW_STATUSES))
        )

    return value


def assess_plate_candidate(
    lab_report: dict[str, Any],
    *,
    candidate_name: str,
    method_id: str | None = None,
    local_graphic: str,
    kindle_graphic: str,
    whole_page: str = "NOT_EVALUATED",
    reviewer: str | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    method=method_for_candidate(
        candidate_name,
        method_id=method_id,
    )

    if method is None:
        raise ValueError(
            f"No admitted optimization method is associated with "
            f"candidate {candidate_name!r}."
        )

    candidates=lab_report.get("candidates",[])

    baseline_matches=[
        item
        for item in candidates
        if item.get("name") == "baseline"
    ]

    candidate_matches=[
        item
        for item in candidates
        if item.get("name") == candidate_name
    ]

    if len(baseline_matches) != 1:
        raise ValueError(
            "Optimization report must contain exactly one baseline."
        )

    if len(candidate_matches) != 1:
        raise ValueError(
            f"Optimization report must contain exactly one "
            f"{candidate_name!r} candidate."
        )

    baseline=baseline_matches[0]
    candidate=candidate_matches[0]

    local_graphic=_review_status(
        "local_graphic",
        local_graphic,
    )

    kindle_graphic=_review_status(
        "kindle_graphic",
        kindle_graphic,
    )

    whole_page=_review_status(
        "whole_page",
        whole_page,
    )

    same_dimensions=(
        baseline["width_px"] == candidate["width_px"]
        and baseline["height_px"] == candidate["height_px"]
    )

    smaller_file=(
        candidate["bytes"] < baseline["bytes"]
    )

    reserve_met=(
        candidate.get("device_status") == "RESERVE MET"
    )

    automatic_checks={
        "same_dimensions":same_dimensions,
        "smaller_file":smaller_file,
        "device_reserve_met":reserve_met,
    }

    automatic_pass=all(automatic_checks.values())

    human_fail=(
        local_graphic == "FAIL"
        or kindle_graphic == "FAIL"
    )

    human_pass=(
        local_graphic == "PASS"
        and kindle_graphic == "PASS"
    )

    if not automatic_pass or human_fail:
        disposition="REJECT"

    elif human_pass:
        disposition="ELIGIBLE_FOR_PLATE_ADMISSION"

    else:
        disposition="REVIEW_OPEN"

    savings_bytes=(
        baseline["bytes"] - candidate["bytes"]
    )

    savings_fraction=(
        savings_bytes / baseline["bytes"]
        if baseline["bytes"]
        else 0
    )

    return {
        "schema":"mfl.plate-optimization-review/1",
        "recorded_utc":datetime.now(
            timezone.utc
        ).isoformat(),
        "component":lab_report.get(
            "component",
            {},
        ),
        "candidate":candidate_name,
        "method":method.to_dict(),
        "review_zone":GRAPHIC_REVIEW_ZONE,
        "automatic_checks":automatic_checks,
        "human_review":{
            "reviewer":reviewer,
            "local_graphic":local_graphic,
            "kindle_graphic":kindle_graphic,
            "whole_page_composition":whole_page,
            "note":note,
        },
        "baseline":{
            "width_px":baseline["width_px"],
            "height_px":baseline["height_px"],
            "bytes":baseline["bytes"],
        },
        "candidate_evidence":{
            "width_px":candidate["width_px"],
            "height_px":candidate["height_px"],
            "bytes":candidate["bytes"],
            "device_status":candidate.get(
                "device_status"
            ),
            "byte_status":candidate.get(
                "byte_status"
            ),
            "savings_bytes":savings_bytes,
            "savings_fraction":savings_fraction,
        },
        "disposition":disposition,
        "automatic_promotion":False,
        "publication_replacement_performed":False,
    }


def write_plate_review(
    record: dict[str, Any],
    destination: str | Path,
) -> Path:
    destination=Path(destination)
    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination.write_text(
        json.dumps(
            record,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    return destination
