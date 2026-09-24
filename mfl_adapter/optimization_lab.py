"""Review-only plate optimization laboratory.

The laboratory produces candidates. It never promotes a candidate into
an EPUB or rewrites an admitted plate.

Techniques are independently implemented with Pillow. External projects
such as KCC may inform which experiments are interesting, but no external
image-processing implementation is incorporated here.
"""
from __future__ import annotations

import html
import io
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageStat

from .device_profiles import (
    DEFAULT_PLANNING_DEVICES,
    MFL_RESERVE_RATIO,
    plan_width,
)
from .profile_planning import (
    PLATE_ROUTES,
    byte_budget_status,
)
from .optimization_policy import (
    GRAPHIC_REVIEW_ZONE,
    method_for_candidate,
)
from .render import deterministic_png_bytes


def _load_profile(path: str | Path) -> dict[str, Any]:
    path=Path(path)

    if not path.is_file():
        raise FileNotFoundError(path)

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def _component(profile: dict[str, Any], key: str) -> dict[str, Any]:
    matches=[
        item
        for item in profile.get("components",[])
        if item.get("key") == key
    ]

    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one component {key!r}; found {len(matches)}."
        )

    component=matches[0]

    if component.get("route") not in PLATE_ROUTES:
        raise ValueError(
            f"{key}: route {component.get('route')!r} is not a plate route."
        )

    return component


def _rgb_image(data: bytes) -> Image.Image:
    with Image.open(io.BytesIO(data)) as image:
        return image.convert("RGB").copy()


def _comparison(
    baseline: Image.Image,
    candidate: Image.Image,
) -> dict[str, Any]:
    candidate_rgb=candidate.convert("RGB")

    if candidate_rgb.size == baseline.size:
        aligned=candidate_rgb
        alignment="same dimensions"
    else:
        aligned=candidate_rgb.resize(
            baseline.size,
            Image.Resampling.LANCZOS,
        )
        alignment=(
            "candidate resized back to baseline dimensions "
            "for engineering comparison only"
        )

    diff=ImageChops.difference(
        baseline,
        aligned,
    )

    stat=ImageStat.Stat(diff)
    extrema=diff.getextrema()

    return {
        "comparison_alignment":alignment,
        "pixel_identical_after_alignment":(
            diff.getbbox() is None
        ),
        "maximum_channel_error":max(
            high
            for low,high in extrema
        ),
        "mean_absolute_error":[
            round(value,6)
            for value in stat.mean
        ],
        "rms_error":[
            round(value,6)
            for value in stat.rms
        ],
    }


def _write_candidate(
    *,
    name: str,
    image: Image.Image,
    baseline: Image.Image,
    destination: Path,
    component: dict[str, Any],
    device_keys: tuple[str, ...],
    reserve_ratio: float,
    purpose: str,
) -> dict[str, Any]:
    data=deterministic_png_bytes(image)

    path=destination/f"{name}.png"
    path.write_bytes(data)

    width,height=image.size

    device_plan=plan_width(
        source_width_px=width,
        display_fraction=component["display_width_percent"]/100,
        device_keys=device_keys,
        reserve_ratio=reserve_ratio,
    )

    byte_status,utilization=byte_budget_status(
        len(data),
        component.get("byte_budget"),
    )

    return {
        "name":name,
        "filename":path.name,
        "purpose":purpose,
        "promotion_status":"REVIEW ONLY",
        "width_px":width,
        "height_px":height,
        "bytes":len(data),
        "byte_status":byte_status,
        "byte_budget_utilization":utilization,
        "device_status":device_plan["worst_status"],
        "device_plan":device_plan,
        "comparison":_comparison(
            baseline,
            image,
        ),
    }


def _palette(image: Image.Image, colors: int) -> Image.Image:
    return image.quantize(
        colors=colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )


def _resize_width(image: Image.Image, width: int) -> Image.Image:
    if width <= 0:
        raise ValueError("Resize width must be positive.")

    height=round(
        image.height * width / image.width
    )

    return image.resize(
        (width,height),
        Image.Resampling.LANCZOS,
    )


def _review_html(
    *,
    key: str,
    candidates: list[dict[str, Any]],
) -> str:
    cards=[]

    for item in candidates:
        cards.append(
            f"""
<section>
<h2>{html.escape(item['name'])}</h2>
<img src="{html.escape(item['filename'])}"
     alt="Review candidate for {html.escape(key)}">
<table>
<tr><th>Purpose</th><td>{html.escape(item['purpose'])}</td></tr>
<tr><th>Dimensions</th><td>{item['width_px']}  {item['height_px']}</td></tr>
<tr><th>Bytes</th><td>{item['bytes']:,}</td></tr>
<tr><th>Byte status</th><td>{html.escape(item['byte_status'])}</td></tr>
<tr><th>Device status</th><td>{html.escape(item['device_status'])}</td></tr>
<tr><th>Promotion</th><td>REVIEW ONLY</td></tr>
</table>
</section>
"""
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(key)} optimization review</title>
<style>
body {{
    font-family: system-ui, sans-serif;
    max-width: 1100px;
    margin: 2rem auto;
    padding: 0 1rem;
    line-height: 1.45;
}}
section {{
    margin: 0 0 3rem;
    border-bottom: 1px solid #999;
    padding-bottom: 2rem;
}}
img {{
    display: block;
    max-width: 100%;
    height: auto;
    margin: 1rem 0;
}}
table {{
    border-collapse: collapse;
}}
th, td {{
    border: 1px solid #aaa;
    padding: 0.4rem 0.6rem;
    text-align: left;
}}
</style>
</head>
<body>
<h1>{html.escape(key)}  optimization laboratory</h1>
<p>
These are review candidates only. No candidate has authority to replace
the admitted plate without human visual acceptance.
</p>
{''.join(cards)}
</body>
</html>
"""


def run_optimization_lab(
    *,
    profile_path: str | Path,
    run_dir: str | Path,
    component_key: str,
    output_dir: str | Path,
    device_keys: tuple[str, ...] = DEFAULT_PLANNING_DEVICES,
    reserve_ratio: float = MFL_RESERVE_RATIO,
) -> dict[str, Any]:
    profile=_load_profile(profile_path)
    component=_component(profile,component_key)

    run_dir=Path(run_dir).resolve()
    output_dir=Path(output_dir).resolve()

    output_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    source=(
        run_dir
        /"plates"
        /f"{component_key}.png"
    )

    if not source.is_file():
        raise FileNotFoundError(source)

    baseline_bytes=source.read_bytes()
    baseline=_rgb_image(baseline_bytes)

    if baseline.width != component["source_width_px"]:
        raise ValueError(
            f"{component_key}: admitted plate width {baseline.width}px "
            f"does not match profile source_width_px "
            f"{component['source_width_px']}px."
        )

    width_plan=plan_width(
        source_width_px=baseline.width,
        display_fraction=component["display_width_percent"]/100,
        device_keys=device_keys,
        reserve_ratio=reserve_ratio,
    )

    reserve_width=(
        width_plan["minimum_source_width_for_all_devices_px"]
    )

    candidates=[]

    baseline_copy=output_dir/"baseline.png"
    baseline_copy.write_bytes(baseline_bytes)

    baseline_status,baseline_utilization=byte_budget_status(
        len(baseline_bytes),
        component.get("byte_budget"),
    )

    candidates.append({
        "name":"baseline",
        "filename":"baseline.png",
        "purpose":"Current admitted plate; comparison authority for this lab.",
        "promotion_status":"CURRENT ADMITTED BASELINE",
        "width_px":baseline.width,
        "height_px":baseline.height,
        "bytes":len(baseline_bytes),
        "byte_status":baseline_status,
        "byte_budget_utilization":baseline_utilization,
        "device_status":width_plan["worst_status"],
        "device_plan":width_plan,
        "comparison":{
            "comparison_alignment":"identity",
            "pixel_identical_after_alignment":True,
            "maximum_channel_error":0,
            "mean_absolute_error":[0.0,0.0,0.0],
            "rms_error":[0.0,0.0,0.0],
        },
    })

    candidates.append(
        _write_candidate(
            name="palette-256",
            image=_palette(baseline,256),
            baseline=baseline,
            destination=output_dir,
            component=component,
            device_keys=device_keys,
            reserve_ratio=reserve_ratio,
            purpose=(
                "Original dimensions; deterministic 256-color palette; "
                "no dithering."
            ),
        )
    )

    reserve_rgb=_resize_width(
        baseline,
        reserve_width,
    )

    candidates.append(
        _write_candidate(
            name="reserve-width-rgb",
            image=reserve_rgb,
            baseline=baseline,
            destination=output_dir,
            component=component,
            device_keys=device_keys,
            reserve_ratio=reserve_ratio,
            purpose=(
                "Downsampled exactly to the MFL reserve-width requirement "
                "for the selected device set."
            ),
        )
    )

    candidates.append(
        _write_candidate(
            name="reserve-width-palette-256",
            image=_palette(reserve_rgb,256),
            baseline=baseline,
            destination=output_dir,
            component=component,
            device_keys=device_keys,
            reserve_ratio=reserve_ratio,
            purpose=(
                "Reserve-width downsample plus deterministic 256-color "
                "palette; no dithering."
            ),
        )
    )

    candidates.append(
        _write_candidate(
            name="grayscale-simulation",
            image=baseline.convert("L"),
            baseline=baseline,
            destination=output_dir,
            component=component,
            device_keys=device_keys,
            reserve_ratio=reserve_ratio,
            purpose=(
                "Grayscale review simulation only; not a promotion candidate."
            ),
        )
    )

    for item in candidates:
        method=method_for_candidate(
            item["name"]
        )

        if method is not None:
            item["optimization_method"]=(
                method.to_dict()
            )
        else:
            item["optimization_method"]=None

    report={
        "schema":"mfl.plate-optimization-lab/1",
        "component":{
            "key":component_key,
            "route":component["route"],
            "display_width_percent":component["display_width_percent"],
            "byte_budget":component.get("byte_budget"),
        },
        "policy":{
            "reserve_ratio":reserve_ratio,
            "device_keys":list(device_keys),
            "reserve_width_px":reserve_width,
            "automatic_promotion":False,
            "tone_changing_experiments":False,
            "crop_changes":False,
            "graphic_review_zone":GRAPHIC_REVIEW_ZONE,
        },
        "candidates":candidates,
    }

    (output_dir/"OPTIMIZATION_REPORT.json").write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        )+"\n",
        encoding="utf-8",
    )

    (output_dir/"REVIEW.html").write_text(
        _review_html(
            key=component_key,
            candidates=candidates,
        ),
        encoding="utf-8",
    )

    return report
