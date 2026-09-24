"""Batch review surface for explicitly selected plate components.

This orchestrates existing per-plate optimization laboratories. It does
not broaden method authority, automatically apply optimization, approve
candidates, or admit assets into builds.

Every component remains independently human-governed.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from .optimization_lab import run_optimization_lab
from .optimization_policy import GRAPHIC_REVIEW_ZONE
from .profile_planning import PLATE_ROUTES
from .device_profiles import (
    DEFAULT_PLANNING_DEVICES,
    MFL_RESERVE_RATIO,
)


def _load_profile(path: str | Path) -> dict[str, Any]:
    path=Path(path)

    if not path.is_file():
        raise FileNotFoundError(path)

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def _candidate(
    report: dict[str, Any],
    name: str,
) -> dict[str, Any]:
    matches=[
        item
        for item in report.get("candidates",[])
        if item.get("name") == name
    ]

    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one candidate {name!r}; "
            f"found {len(matches)}."
        )

    return matches[0]


def _batch_html(
    *,
    profile_id: str | None,
    summaries: list[dict[str, Any]],
) -> str:
    sections=[]

    for item in summaries:
        key=item["key"]

        sections.append(
            f"""
<section>
<h2>{html.escape(key)}</h2>

<div class="pair">
<figure>
<img src="{html.escape(key)}/baseline.png"
     alt="Baseline plate for {html.escape(key)}">
<figcaption>
Baseline  {item['baseline_bytes']:,} bytes
</figcaption>
</figure>

<figure>
<img src="{html.escape(key)}/palette-256.png"
     alt="Palette-256 review candidate for {html.escape(key)}">
<figcaption>
Palette-256  {item['palette_bytes']:,} bytes
</figcaption>
</figure>
</div>

<table>
<tr>
<th>Route</th>
<td>{html.escape(item['route'])}</td>
</tr>
<tr>
<th>Savings</th>
<td>
{item['savings_bytes']:,} bytes
({item['savings_percent']:.1f}%)
</td>
</tr>
<tr>
<th>Device status</th>
<td>{html.escape(item['device_status'])}</td>
</tr>
<tr>
<th>Byte status</th>
<td>{html.escape(item['byte_status'])}</td>
</tr>
<tr>
<th>Method</th>
<td>{html.escape(item['method_status'])}</td>
</tr>
<tr>
<th>Disposition</th>
<td>REVIEW OPEN</td>
</tr>
</table>

<p>
<a href="{html.escape(key)}/REVIEW.html">
Open full candidate laboratory for {html.escape(key)}
</a>
</p>
</section>
"""
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>MFL batch plate optimization review</title>
<style>
body {{
    font-family: system-ui, sans-serif;
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
    line-height: 1.45;
}}
section {{
    border-top: 1px solid #999;
    padding: 2rem 0;
}}
.pair {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    align-items: start;
}}
figure {{
    margin: 0;
}}
img {{
    display: block;
    max-width: 100%;
    height: auto;
}}
figcaption {{
    margin-top: 0.5rem;
}}
table {{
    border-collapse: collapse;
    margin-top: 1.25rem;
}}
th, td {{
    border: 1px solid #aaa;
    padding: 0.4rem 0.6rem;
    text-align: left;
}}
.notice {{
    padding: 1rem;
    border: 1px solid #999;
}}
@media (max-width: 760px) {{
    .pair {{
        grid-template-columns: 1fr;
    }}
}}
</style>
</head>
<body>

<h1>Batch plate optimization review</h1>

<p><strong>Profile:</strong> {html.escape(str(profile_id))}</p>

<div class="notice">
<p>
This is a review surface only. No candidate is automatically applied,
promoted, or admitted.
</p>
<p>
Judge the contents inside each graphic: typography, geometry, crop,
negative space, color, tone, and whether the relational proposition
is preserved. Surrounding Kindle page composition is a separate gate.
</p>
</div>

{''.join(sections)}

</body>
</html>
"""


def run_batch_optimization_lab(
    *,
    profile_path: str | Path,
    run_dir: str | Path,
    component_keys: list[str] | tuple[str, ...],
    output_dir: str | Path,
    device_keys: tuple[str, ...] = DEFAULT_PLANNING_DEVICES,
    reserve_ratio: float = MFL_RESERVE_RATIO,
) -> dict[str, Any]:
    profile_path=Path(profile_path).resolve()
    run_dir=Path(run_dir).resolve()
    output_dir=Path(output_dir).resolve()

    keys=list(component_keys)

    if not keys:
        raise ValueError(
            "At least one explicit component is required."
        )

    if len(keys) != len(set(keys)):
        raise ValueError(
            "Batch component keys must be unique."
        )

    if output_dir.exists():
        raise FileExistsError(output_dir)

    profile=_load_profile(profile_path)

    components={
        item.get("key"):item
        for item in profile.get("components",[])
    }

    for key in keys:
        if key not in components:
            raise ValueError(
                f"Unknown profile component {key!r}."
            )

        route=components[key].get("route")

        if route not in PLATE_ROUTES:
            raise ValueError(
                f"{key}: route {route!r} is not a plate route."
            )

        plate=run_dir/"plates"/f"{key}.png"

        if not plate.is_file():
            raise FileNotFoundError(plate)

    output_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    summaries=[]
    reports={}

    for key in keys:
        component_dir=output_dir/key

        report=run_optimization_lab(
            profile_path=profile_path,
            run_dir=run_dir,
            component_key=key,
            output_dir=component_dir,
            device_keys=device_keys,
            reserve_ratio=reserve_ratio,
        )

        reports[key]=report

        baseline=_candidate(
            report,
            "baseline",
        )

        palette=_candidate(
            report,
            "palette-256",
        )

        method=palette.get(
            "optimization_method"
        ) or {}

        savings=(
            baseline["bytes"]
            - palette["bytes"]
        )

        savings_fraction=(
            savings / baseline["bytes"]
            if baseline["bytes"]
            else 0
        )

        summaries.append({
            "key":key,
            "route":report[
                "component"
            ]["route"],
            "baseline_bytes":baseline[
                "bytes"
            ],
            "palette_bytes":palette[
                "bytes"
            ],
            "savings_bytes":savings,
            "savings_fraction":savings_fraction,
            "savings_percent":(
                savings_fraction * 100
            ),
            "same_dimensions":(
                baseline["width_px"]
                == palette["width_px"]
                and baseline["height_px"]
                == palette["height_px"]
            ),
            "device_status":palette.get(
                "device_status"
            ),
            "byte_status":palette.get(
                "byte_status"
            ),
            "method_id":method.get(
                "method_id"
            ),
            "method_status":method.get(
                "method_status",
                "NO ADMITTED METHOD",
            ),
            "review_status":"OPEN",
            "automatic_application":False,
            "automatic_promotion":False,
        })

    batch={
        "schema":"mfl.batch-optimization-lab/1",
        "profile":{
            "path":str(profile_path),
            "profile_id":profile.get(
                "profile_id"
            ),
            "profile_version":profile.get(
                "profile_version"
            ),
        },
        "source_run":str(run_dir),
        "policy":{
            "component_selection":"explicit only",
            "automatic_application":False,
            "automatic_promotion":False,
            "review_zone":GRAPHIC_REVIEW_ZONE,
            "device_keys":list(device_keys),
            "reserve_ratio":reserve_ratio,
        },
        "summary":{
            "component_count":len(summaries),
            "baseline_bytes":sum(
                item["baseline_bytes"]
                for item in summaries
            ),
            "palette_bytes":sum(
                item["palette_bytes"]
                for item in summaries
            ),
            "savings_bytes":sum(
                item["savings_bytes"]
                for item in summaries
            ),
        },
        "components":summaries,
    }

    baseline_total=batch[
        "summary"
    ]["baseline_bytes"]

    savings_total=batch[
        "summary"
    ]["savings_bytes"]

    batch["summary"]["savings_fraction"]=(
        savings_total / baseline_total
        if baseline_total
        else 0
    )

    (output_dir/"BATCH_REPORT.json").write_text(
        json.dumps(
            batch,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    (output_dir/"BATCH_REVIEW.html").write_text(
        _batch_html(
            profile_id=profile.get(
                "profile_id"
            ),
            summaries=summaries,
        ),
        encoding="utf-8",
    )

    return batch
