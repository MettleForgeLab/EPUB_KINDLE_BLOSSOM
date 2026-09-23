"""Adaptation-profile device planning.

The profile remains adaptation authority. This module reads its existing
plate routes rather than creating a parallel routing vocabulary.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image

from .device_profiles import (
    DEFAULT_PLANNING_DEVICES,
    MFL_RESERVE_RATIO,
    plan_width,
)


PLATE_ROUTES = {
    "SMALL PLATE",
    "MEDIUM PLATE",
    "FIELD PLATE",
    "OPENING PLATE",
}

MFL_OVERBUILT_HEADROOM = 1.50
MFL_NEAR_BUDGET_FRACTION = 0.90


def _load_profile(path: str | Path) -> dict[str, Any]:
    path=Path(path)

    if not path.is_file():
        raise FileNotFoundError(path)

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def _engineering_status(
    *,
    device_status: str,
    source_width_px: int,
    reserve_width_px: int,
    overbuilt_headroom: float,
) -> str:
    if device_status != "RESERVE MET":
        return device_status

    headroom=source_width_px / reserve_width_px

    if headroom >= overbuilt_headroom:
        return "OVERBUILT"

    return "RESERVE MET"


def byte_budget_status(
    actual_bytes: int,
    budget_bytes: int | None,
    *,
    near_fraction: float = MFL_NEAR_BUDGET_FRACTION,
) -> tuple[str, float | None]:
    """Classify image weight without turning economics into correctness."""
    if actual_bytes < 0:
        raise ValueError("actual_bytes cannot be negative.")

    if budget_bytes is None:
        return "NO BUDGET", None

    if budget_bytes <= 0:
        raise ValueError("budget_bytes must be positive.")

    if not 0 < near_fraction <= 1:
        raise ValueError(
            "near_fraction must be greater than 0 and at most 1."
        )

    utilization=actual_bytes / budget_bytes

    if utilization > 1:
        return "OVER BUDGET", utilization

    if utilization >= near_fraction:
        return "NEAR BUDGET", utilization

    return "WITHIN BUDGET", utilization


def require_pre_render_resolved(plan: dict[str, Any]) -> None:
    under=[
        item["key"]
        for item in plan["components"]
        if item["planning_status"] == "UNDER-RESOLVED"
    ]

    if under:
        raise ValueError(
            "Under-resolved plate plan: "
            + ", ".join(under)
        )


def build_findings(plan: dict[str, Any]) -> list[dict[str, Any]]:
    findings=[]

    for item in plan["components"]:
        key=item["key"]
        planning=item["planning_status"]
        byte_status=item.get("byte_status")

        if planning == "NATIVE COVERAGE":
            findings.append({
                "component":key,
                "kind":"device-resolution",
                "level":"INFO",
                "status":planning,
                "message":(
                    "Plate covers native demand but does not meet "
                    "the MFL reserve ratio."
                ),
            })

        elif planning == "OVERBUILT":
            findings.append({
                "component":key,
                "kind":"device-resolution",
                "level":"INFO",
                "status":planning,
                "message":(
                    "Plate materially exceeds the already-reserved "
                    "pixel requirement; optimization may be possible."
                ),
            })

        if byte_status == "NEAR BUDGET":
            findings.append({
                "component":key,
                "kind":"image-weight",
                "level":"WARNING",
                "status":byte_status,
                "message":(
                    "Plate uses at least 90% of its configured "
                    "byte budget."
                ),
            })

        elif byte_status == "OVER BUDGET":
            findings.append({
                "component":key,
                "kind":"image-weight",
                "level":"WARNING",
                "status":byte_status,
                "message":(
                    "Plate exceeds its configured byte budget. "
                    "Build may proceed, but publishing weight "
                    "requires review."
                ),
            })

    return findings


def _actual_plate(
    run_dir: Path | None,
    key: str,
    expected_width_px: int,
) -> dict[str, Any] | None:
    if run_dir is None:
        return None

    plate=run_dir/"plates"/f"{key}.png"

    if not plate.is_file():
        raise FileNotFoundError(
            f"Expected rendered plate was not found: {plate}"
        )

    with Image.open(plate) as image:
        width,height=image.size

    if width != expected_width_px:
        raise ValueError(
            f"{key}: rendered width {width}px does not match "
            f"profile source_width_px {expected_width_px}px."
        )

    return {
        "path":str(plate.resolve()),
        "width_px":width,
        "height_px":height,
        "aspect_ratio":width / height,
        "bytes":plate.stat().st_size,
    }


def plan_component(
    component: dict[str, Any],
    *,
    run_dir: str | Path | None = None,
    device_keys: tuple[str, ...] = DEFAULT_PLANNING_DEVICES,
    reserve_ratio: float = MFL_RESERVE_RATIO,
    overbuilt_headroom: float = MFL_OVERBUILT_HEADROOM,
) -> dict[str, Any]:
    key=component["key"]
    route=component["route"]

    base={
        "key":key,
        "route":route,
        "reason":component.get("reason"),
    }

    if route not in PLATE_ROUTES:
        return {
            **base,
            "planning_status":"NOT APPLICABLE",
            "note":"Component remains live; no plate pixel plan is required.",
        }

    width=component.get("source_width_px")
    percent=component.get("display_width_percent")

    if not isinstance(width,int) or width <= 0:
        raise ValueError(
            f"{key}: plate route requires positive source_width_px."
        )

    if not isinstance(percent,(int,float)) or not 0 < percent <= 100:
        raise ValueError(
            f"{key}: plate route requires display_width_percent "
            "between 0 and 100."
        )

    width_plan=plan_width(
        source_width_px=width,
        display_fraction=percent / 100,
        device_keys=device_keys,
        reserve_ratio=reserve_ratio,
    )

    reserve_width=(
        width_plan["minimum_source_width_for_all_devices_px"]
    )

    engineering_status=_engineering_status(
        device_status=width_plan["worst_status"],
        source_width_px=width,
        reserve_width_px=reserve_width,
        overbuilt_headroom=overbuilt_headroom,
    )

    run_path=Path(run_dir).resolve() if run_dir else None

    actual=_actual_plate(
        run_path,
        key,
        width,
    )

    byte_budget=component.get("byte_budget")

    if actual is None:
        byte_status="NOT MEASURED"
        byte_utilization=None
    else:
        byte_status,byte_utilization=byte_budget_status(
            actual["bytes"],
            byte_budget,
        )

    return {
        **base,
        "planning_status":engineering_status,
        "display_width_percent":percent,
        "source_width_px":width,
        "minimum_source_width_for_reserve_px":reserve_width,
        "reserve_headroom_ratio":width / reserve_width,
        "overbuilt_headroom_threshold":overbuilt_headroom,
        "byte_budget":byte_budget,
        "byte_status":byte_status,
        "byte_budget_utilization":byte_utilization,
        "actual_plate":actual,
        "device_plan":width_plan,
    }


def plan_profile(
    profile_path: str | Path,
    *,
    run_dir: str | Path | None = None,
    device_keys: tuple[str, ...] = DEFAULT_PLANNING_DEVICES,
    reserve_ratio: float = MFL_RESERVE_RATIO,
    overbuilt_headroom: float = MFL_OVERBUILT_HEADROOM,
) -> dict[str, Any]:
    profile=_load_profile(profile_path)

    components=[
        plan_component(
            component,
            run_dir=run_dir,
            device_keys=device_keys,
            reserve_ratio=reserve_ratio,
            overbuilt_headroom=overbuilt_headroom,
        )
        for component in profile.get("components",[])
    ]

    plated=[
        item
        for item in components
        if item["route"] in PLATE_ROUTES
    ]

    counts={}

    for item in components:
        status=item["planning_status"]
        counts[status]=counts.get(status,0)+1

    return {
        "schema":"mfl.profile-device-plan/1",
        "profile":{
            "profile_id":profile.get("profile_id"),
            "profile_version":profile.get("profile_version"),
            "mode":profile.get("mode"),
        },
        "policy":{
            "reserve_ratio":reserve_ratio,
            "overbuilt_headroom_threshold":overbuilt_headroom,
            "device_keys":list(device_keys),
            "css_viewport_claim":False,
        },
        "summary":{
            "component_count":len(components),
            "plate_count":len(plated),
            "status_counts":counts,
        },
        "components":components,
    }
