"""Named physical-pixel targets used for plate suitability planning.

These are not CSS viewport dimensions and do not predict Kindle pagination.
The initial Kindle values are transcribed from the current Kindle Comic
Converter device-profile table and are kept separate from MFL logical
viewport/vertical-footprint policies.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class DeviceProfile:
    key: str
    label: str
    width_px: int
    height_px: int
    family: str = "Kindle"
    evidence: str = "KCC device profile; engineering reference only"

    @property
    def portrait_pixels(self) -> tuple[int, int]:
        return (self.width_px, self.height_px)

    def to_dict(self) -> dict:
        return asdict(self)


DEVICE_PROFILES = {
    "kindle-11": DeviceProfile(
        "kindle-11", "Kindle 11", 1072, 1448
    ),
    "paperwhite-5": DeviceProfile(
        "paperwhite-5", "Kindle Paperwhite 5 / Signature Edition",
        1236, 1648
    ),
    "paperwhite-6": DeviceProfile(
        "paperwhite-6", "Kindle Paperwhite 6",
        1272, 1696
    ),
    "colorsoft": DeviceProfile(
        "colorsoft", "Kindle Colorsoft",
        1272, 1696
    ),
    "scribe-1-2": DeviceProfile(
        "scribe-1-2", "Kindle Scribe 1 / 2",
        1860, 2480
    ),
    "scribe-3": DeviceProfile(
        "scribe-3", "Kindle Scribe 3",
        1986, 2648
    ),
}


def get_device_profile(key: str) -> DeviceProfile:
    try:
        return DEVICE_PROFILES[key]
    except KeyError as exc:
        known = ", ".join(sorted(DEVICE_PROFILES))
        raise KeyError(
            f"Unknown device profile {key!r}. Known profiles: {known}"
        ) from exc


def list_device_profiles() -> list[dict]:
    return [
        DEVICE_PROFILES[key].to_dict()
        for key in sorted(DEVICE_PROFILES)
    ]


def plate_pixel_report(
    width_px: int,
    height_px: int,
    device_key: str,
) -> dict:
    """Describe source-plate oversampling relative to a physical target.

    This deliberately does not decide CSS display width.
    """
    if width_px <= 0 or height_px <= 0:
        raise ValueError("Plate dimensions must be positive.")

    device = get_device_profile(device_key)

    scale_x = width_px / device.width_px
    scale_y = height_px / device.height_px

    return {
        "device": device.to_dict(),
        "plate_width_px": width_px,
        "plate_height_px": height_px,
        "width_ratio_to_device": scale_x,
        "height_ratio_to_device": scale_y,
        "covers_device_width": width_px >= device.width_px,
        "covers_device_height": height_px >= device.height_px,
    }
