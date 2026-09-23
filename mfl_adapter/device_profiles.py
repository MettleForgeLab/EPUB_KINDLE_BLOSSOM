"""Device-aware plate planning.

Physical device dimensions are engineering references only. They are
not CSS viewport dimensions and do not predict Kindle pagination.

The initial Kindle dimensions are transcribed from the current Kindle
Comic Converter device profile table. MFL reserve thresholds are our
own engineering policy.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import ceil


MFL_RESERVE_RATIO = 1.25


@dataclass(frozen=True)
class DeviceProfile:
    key: str
    label: str
    width_px: int
    height_px: int
    family: str = "Kindle"
    evidence: str = (
        "KCC device profile; physical-pixel engineering reference only"
    )

    def to_dict(self) -> dict:
        return asdict(self)


DEVICE_PROFILES = {
    "kindle-11": DeviceProfile(
        "kindle-11",
        "Kindle 11",
        1072,
        1448,
    ),
    "paperwhite-5": DeviceProfile(
        "paperwhite-5",
        "Kindle Paperwhite 5 / Signature Edition",
        1236,
        1648,
    ),
    "paperwhite-6": DeviceProfile(
        "paperwhite-6",
        "Kindle Paperwhite 6",
        1272,
        1696,
    ),
    "colorsoft": DeviceProfile(
        "colorsoft",
        "Kindle Colorsoft",
        1272,
        1696,
    ),
    "scribe-1-2": DeviceProfile(
        "scribe-1-2",
        "Kindle Scribe 1 / 2",
        1860,
        2480,
    ),
    "scribe-3": DeviceProfile(
        "scribe-3",
        "Kindle Scribe 3",
        1986,
        2648,
    ),
}


DEFAULT_PLANNING_DEVICES = (
    "paperwhite-6",
    "colorsoft",
    "scribe-3",
)


def get_device_profile(key: str) -> DeviceProfile:
    try:
        return DEVICE_PROFILES[key]
    except KeyError as exc:
        known=", ".join(sorted(DEVICE_PROFILES))
        raise KeyError(
            f"Unknown device profile {key!r}. Known profiles: {known}"
        ) from exc


def list_device_profiles() -> list[dict]:
    return [
        DEVICE_PROFILES[key].to_dict()
        for key in sorted(DEVICE_PROFILES)
    ]


def _require_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive.")


def _require_fraction(name: str, value: float) -> None:
    if not 0 < value <= 1:
        raise ValueError(
            f"{name} must be greater than 0 and at most 1."
        )


def coverage_status(
    ratio: float,
    *,
    reserve_ratio: float = MFL_RESERVE_RATIO,
) -> str:
    _require_positive("ratio", ratio)
    _require_positive("reserve_ratio", reserve_ratio)

    if ratio >= reserve_ratio:
        return "RESERVE MET"

    if ratio >= 1.0:
        return "NATIVE COVERAGE"

    return "UNDER-RESOLVED"



def plate_pixel_report(
    width_px: int,
    height_px: int,
    device_key: str,
) -> dict:
    """Backward-compatible 0.3 physical-pixel comparison.

    This reports raw plate dimensions relative to a named physical
    device profile. It intentionally makes no CSS viewport claim.

    New 0.4 planning code should normally use plan_plate_for_device().
    """
    _require_positive("width_px", width_px)
    _require_positive("height_px", height_px)

    device = get_device_profile(device_key)

    return {
        "device": device.to_dict(),
        "plate_width_px": width_px,
        "plate_height_px": height_px,
        "width_ratio_to_device": (
            width_px / device.width_px
        ),
        "height_ratio_to_device": (
            height_px / device.height_px
        ),
        "covers_device_width": (
            width_px >= device.width_px
        ),
        "covers_device_height": (
            height_px >= device.height_px
        ),
    }



def plan_width_for_device(
    *,
    source_width_px: int,
    display_fraction: float,
    device_key: str,
    reserve_ratio: float = MFL_RESERVE_RATIO,
) -> dict:
    """Plan horizontal plate coverage for one physical device class.

    This is the pre-render planner. It deliberately requires no source
    height and makes no CSS viewport claim.
    """
    _require_positive("source_width_px", source_width_px)
    _require_fraction("display_fraction", display_fraction)
    _require_positive("reserve_ratio", reserve_ratio)

    device=get_device_profile(device_key)

    demand_width=device.width_px * display_fraction
    coverage=source_width_px / demand_width

    return {
        "device":device.to_dict(),
        "display_fraction":display_fraction,
        "planning_basis":{
            "kind":"physical-screen-width upper-bound proxy",
            "css_viewport_claim":False,
        },
        "source_width_px":source_width_px,
        "estimated_demand_width_px":demand_width,
        "required_width_px":{
            "native":ceil(demand_width),
            "reserve":ceil(demand_width * reserve_ratio),
        },
        "coverage_ratio":coverage,
        "reserve_ratio":reserve_ratio,
        "status":coverage_status(
            coverage,
            reserve_ratio=reserve_ratio,
        ),
    }


def plan_width(
    *,
    source_width_px: int,
    display_fraction: float,
    device_keys: tuple[str, ...] = DEFAULT_PLANNING_DEVICES,
    reserve_ratio: float = MFL_RESERVE_RATIO,
) -> dict:
    if not device_keys:
        raise ValueError("At least one device profile is required.")

    plans=[
        plan_width_for_device(
            source_width_px=source_width_px,
            display_fraction=display_fraction,
            device_key=key,
            reserve_ratio=reserve_ratio,
        )
        for key in device_keys
    ]

    rank={
        "UNDER-RESOLVED":0,
        "NATIVE COVERAGE":1,
        "RESERVE MET":2,
    }

    worst=min(
        plans,
        key=lambda item:rank[item["status"]],
    )

    maximum_required=max(
        item["required_width_px"]["reserve"]
        for item in plans
    )

    return {
        "source_width_px":source_width_px,
        "display_fraction":display_fraction,
        "reserve_ratio":reserve_ratio,
        "devices":plans,
        "worst_status":worst["status"],
        "minimum_source_width_for_all_devices_px":maximum_required,
    }


def plan_plate_for_device(
    *,
    source_width_px: int,
    source_height_px: int,
    display_fraction: float,
    device_key: str,
    reserve_ratio: float = MFL_RESERVE_RATIO,
) -> dict:
    """Plan one plate against one physical device class.

    ``display_fraction`` is the intended fraction of the available
    reading column.

    Because the actual reading column is normally narrower than the
    physical screen, using ``device.width_px * display_fraction`` is a
    conservative upper-bound demand proxy. Meeting reserve here does
    not assert Kindle CSS pixel equivalence.
    """
    _require_positive("source_width_px", source_width_px)
    _require_positive("source_height_px", source_height_px)
    _require_fraction("display_fraction", display_fraction)
    _require_positive("reserve_ratio", reserve_ratio)

    device=get_device_profile(device_key)

    demand_width=device.width_px * display_fraction

    source_ratio=source_width_px / demand_width

    required_native_width=ceil(demand_width)
    required_reserve_width=ceil(
        demand_width * reserve_ratio
    )

    aspect_ratio=source_width_px / source_height_px
    projected_height=demand_width / aspect_ratio

    return {
        "device":device.to_dict(),
        "display_fraction":display_fraction,
        "planning_basis":{
            "kind":"physical-screen-width upper-bound proxy",
            "css_viewport_claim":False,
        },
        "source":{
            "width_px":source_width_px,
            "height_px":source_height_px,
            "aspect_ratio":aspect_ratio,
        },
        "estimated_demand":{
            "width_px":demand_width,
            "height_px":projected_height,
        },
        "required_width_px":{
            "native":required_native_width,
            "reserve":required_reserve_width,
        },
        "coverage_ratio":source_ratio,
        "reserve_ratio":reserve_ratio,
        "status":coverage_status(
            source_ratio,
            reserve_ratio=reserve_ratio,
        ),
    }


def plan_plate(
    *,
    source_width_px: int,
    source_height_px: int,
    display_fraction: float,
    device_keys: tuple[str, ...] = DEFAULT_PLANNING_DEVICES,
    reserve_ratio: float = MFL_RESERVE_RATIO,
) -> dict:
    if not device_keys:
        raise ValueError("At least one device profile is required.")

    plans=[
        plan_plate_for_device(
            source_width_px=source_width_px,
            source_height_px=source_height_px,
            display_fraction=display_fraction,
            device_key=key,
            reserve_ratio=reserve_ratio,
        )
        for key in device_keys
    ]

    rank={
        "UNDER-RESOLVED":0,
        "NATIVE COVERAGE":1,
        "RESERVE MET":2,
    }

    worst=min(
        plans,
        key=lambda item: rank[item["status"]],
    )

    maximum_required=max(
        item["required_width_px"]["reserve"]
        for item in plans
    )

    return {
        "source_width_px":source_width_px,
        "source_height_px":source_height_px,
        "display_fraction":display_fraction,
        "reserve_ratio":reserve_ratio,
        "devices":plans,
        "worst_status":worst["status"],
        "minimum_source_width_for_all_devices_px":maximum_required,
    }
