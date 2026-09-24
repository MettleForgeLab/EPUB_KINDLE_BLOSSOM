"""Explicit, human-authorized plate admission.

Optimization eligibility and publication admission are separate acts.
An admission packet locks the profile, review, rendered baseline, candidate
asset, method, and human authorization.

No fuzzy lookup. No latest-candidate behavior. Any identity drift stops.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Any

from PIL import Image

from .core import digest
from .profile_planning import byte_budget_status


ADMISSION_SCHEMA = "mfl.plate-admission/1"
APPLIED_SCHEMA = "mfl.plate-admissions-applied/1"


def _json(path: str | Path) -> dict[str, Any]:
    path=Path(path)

    if not path.is_file():
        raise FileNotFoundError(path)

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def _image_info(path: str | Path) -> dict[str, Any]:
    path=Path(path)

    if not path.is_file():
        raise FileNotFoundError(path)

    data=path.read_bytes()

    with Image.open(path) as image:
        width,height=image.size

    return {
        "sha256":digest(data),
        "bytes":len(data),
        "width_px":width,
        "height_px":height,
    }


def _profile_component(
    profile: dict[str, Any],
    key: str,
) -> dict[str, Any]:
    matches=[
        item
        for item in profile.get("components",[])
        if item.get("key") == key
    ]

    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one profile component {key!r}; "
            f"found {len(matches)}."
        )

    return matches[0]


def create_plate_admission(
    *,
    review_path: str | Path,
    candidate_path: str | Path,
    baseline_path: str | Path,
    profile_path: str | Path,
    output_dir: str | Path,
    authorized_by: str,
    authorization: str,
) -> dict[str, Any]:
    if authorization != "ADMIT":
        raise ValueError(
            "Explicit authorization token must be exactly 'ADMIT'."
        )

    authorized_by=authorized_by.strip()

    if not authorized_by:
        raise ValueError("authorized_by cannot be empty.")

    review_path=Path(review_path).resolve()
    candidate_path=Path(candidate_path).resolve()
    baseline_path=Path(baseline_path).resolve()
    profile_path=Path(profile_path).resolve()
    output_dir=Path(output_dir).resolve()

    if output_dir.exists():
        raise FileExistsError(output_dir)

    review=_json(review_path)
    profile=_json(profile_path)

    if (
        review.get("disposition")
        != "ELIGIBLE_FOR_PLATE_ADMISSION"
    ):
        raise ValueError(
            "Review is not eligible for plate admission."
        )

    if review.get("automatic_promotion") is not False:
        raise ValueError(
            "Review must explicitly preserve non-automatic promotion."
        )

    if (
        review.get("publication_replacement_performed")
        is not False
    ):
        raise ValueError(
            "Review unexpectedly claims publication replacement."
        )

    human=review.get("human_review",{})

    if human.get("local_graphic") != "PASS":
        raise ValueError("Local graphic review is not PASS.")

    if human.get("kindle_graphic") != "PASS":
        raise ValueError("Kindle graphic review is not PASS.")

    method=review.get("method",{})

    if method.get("method_status") != "ADMITTED METHOD":
        raise ValueError(
            "Optimization method is not admitted."
        )

    if method.get("automatic_promotion") is not False:
        raise ValueError(
            "Optimization method must remain non-automatic."
        )

    component=review.get("component",{})
    key=component.get("key")

    if not key:
        raise ValueError(
            "Review does not identify a component key."
        )

    profile_component=_profile_component(
        profile,
        key,
    )

    if profile_component.get("route") != component.get("route"):
        raise ValueError(
            f"{key}: review route and profile route differ."
        )

    candidate_info=_image_info(candidate_path)
    baseline_info=_image_info(baseline_path)

    review_candidate=review.get(
        "candidate_evidence",
        {},
    )

    review_baseline=review.get(
        "baseline",
        {},
    )

    for field in (
        "width_px",
        "height_px",
        "bytes",
    ):
        if candidate_info[field] != review_candidate.get(field):
            raise ValueError(
                f"Candidate {field} does not match review evidence."
            )

        if baseline_info[field] != review_baseline.get(field):
            raise ValueError(
                f"Baseline {field} does not match review evidence."
            )

    if method.get("preserves_dimensions"):
        if (
            candidate_info["width_px"]
            != baseline_info["width_px"]
            or candidate_info["height_px"]
            != baseline_info["height_px"]
        ):
            raise ValueError(
                "Method requires dimensions to be preserved."
            )

    if candidate_info["bytes"] >= baseline_info["bytes"]:
        raise ValueError(
            "Candidate is not smaller than the locked baseline."
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    review_copy=output_dir/"PLATE_REVIEW.json"
    candidate_copy=output_dir/"candidate.png"
    baseline_copy=output_dir/"baseline.png"

    shutil.copyfile(
        review_path,
        review_copy,
    )

    shutil.copyfile(
        candidate_path,
        candidate_copy,
    )

    shutil.copyfile(
        baseline_path,
        baseline_copy,
    )

    record={
        "schema":ADMISSION_SCHEMA,
        "authorized_utc":datetime.now(
            timezone.utc
        ).isoformat(),
        "authorization":{
            "decision":"ADMIT",
            "authorized_by":authorized_by,
            "scope":(
                "Use the locked candidate plate only in builds "
                "whose profile identity and rendered baseline "
                "match this admission packet exactly."
            ),
        },
        "component":{
            "key":key,
            "route":component.get("route"),
        },
        "profile":{
            "filename":profile_path.name,
            "profile_id":profile.get("profile_id"),
            "profile_version":profile.get("profile_version"),
            "sha256":digest(profile_path.read_bytes()),
        },
        "method":{
            "method_id":method.get("method_id"),
            "method_status":method.get("method_status"),
        },
        "review":{
            "filename":review_copy.name,
            "sha256":digest(review_copy.read_bytes()),
            "disposition":review.get("disposition"),
            "local_graphic":human.get("local_graphic"),
            "kindle_graphic":human.get("kindle_graphic"),
            "whole_page_composition":human.get(
                "whole_page_composition"
            ),
        },
        "baseline":{
            "filename":baseline_copy.name,
            **_image_info(baseline_copy),
        },
        "candidate":{
            "candidate_name":review.get("candidate"),
            "filename":candidate_copy.name,
            **_image_info(candidate_copy),
        },
        "automatic_promotion":False,
        "publication_replacement_authorized":True,
    }

    admission_path=output_dir/"PLATE_ADMISSION.json"

    admission_path.write_text(
        json.dumps(
            record,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    return record


def verify_admission_packet(
    admission_path: str | Path,
    *,
    profile_path: str | Path,
) -> dict[str, Any]:
    admission_path=Path(admission_path).resolve()
    profile_path=Path(profile_path).resolve()

    record=_json(admission_path)

    if record.get("schema") != ADMISSION_SCHEMA:
        raise ValueError(
            "Unsupported plate-admission schema."
        )

    if (
        record.get("authorization",{}).get("decision")
        != "ADMIT"
    ):
        raise ValueError(
            "Admission record is not explicitly authorized."
        )

    if (
        record.get("publication_replacement_authorized")
        is not True
    ):
        raise ValueError(
            "Admission record does not authorize replacement."
        )

    if record.get("automatic_promotion") is not False:
        raise ValueError(
            "Admission record must preserve non-automatic promotion."
        )

    expected_profile=record.get("profile",{})

    actual_profile_sha=digest(
        profile_path.read_bytes()
    )

    if expected_profile.get("sha256") != actual_profile_sha:
        raise ValueError(
            "Admission profile SHA-256 does not match current profile."
        )

    packet_dir=admission_path.parent

    review_path=packet_dir/record["review"]["filename"]
    candidate_path=packet_dir/record["candidate"]["filename"]
    baseline_path=packet_dir/record["baseline"]["filename"]

    if digest(review_path.read_bytes()) != record["review"]["sha256"]:
        raise ValueError(
            "Admission review SHA-256 mismatch."
        )

    review=_json(review_path)

    if (
        review.get("disposition")
        != "ELIGIBLE_FOR_PLATE_ADMISSION"
    ):
        raise ValueError(
            "Locked review is no longer admission-eligible."
        )

    if (
        review.get("method",{}).get("method_id")
        != record.get("method",{}).get("method_id")
    ):
        raise ValueError(
            "Admission method does not match locked review."
        )

    if (
        review.get("component",{}).get("key")
        != record.get("component",{}).get("key")
    ):
        raise ValueError(
            "Admission component does not match locked review."
        )

    for label,path in (
        ("candidate",candidate_path),
        ("baseline",baseline_path),
    ):
        actual=_image_info(path)
        expected=record[label]

        for field in (
            "sha256",
            "bytes",
            "width_px",
            "height_px",
        ):
            if actual[field] != expected.get(field):
                raise ValueError(
                    f"Admission {label} {field} mismatch."
                )

    return {
        "record":record,
        "record_sha256":digest(
            admission_path.read_bytes()
        ),
        "record_path":str(admission_path),
        "review_path":review_path,
        "candidate_path":candidate_path,
        "baseline_path":baseline_path,
    }


def apply_plate_admissions(
    admission_paths: list[str | Path],
    *,
    profile_path: str | Path,
    run_dir: str | Path,
    rendering: dict[str, Any],
) -> dict[str, Any]:
    run_dir=Path(run_dir).resolve()
    profile_path=Path(profile_path).resolve()

    if not admission_paths:
        return {
            "schema":APPLIED_SCHEMA,
            "admission_count":0,
            "admissions":[],
        }

    rendered={
        item["key"]:item
        for item in rendering.get("plates",[])
    }

    seen=set()
    applied=[]

    for admission_path in admission_paths:
        verified=verify_admission_packet(
            admission_path,
            profile_path=profile_path,
        )

        record=verified["record"]
        key=record["component"]["key"]

        if key in seen:
            raise ValueError(
                f"Duplicate admission for component {key!r}."
            )

        seen.add(key)

        if key not in rendered:
            raise ValueError(
                f"Admission targets unrendered plate {key!r}."
            )

        plate=run_dir/"plates"/f"{key}.png"

        if not plate.is_file():
            raise FileNotFoundError(plate)

        baseline_sha=digest(
            plate.read_bytes()
        )

        if baseline_sha != record["baseline"]["sha256"]:
            raise ValueError(
                f"{key}: rendered baseline SHA-256 does not match "
                "the admission packet."
            )

        evidence=(
            run_dir
            /"admission-evidence"
            /key
        )

        evidence.mkdir(
            parents=True,
            exist_ok=False,
        )

        shutil.copyfile(
            plate,
            evidence/"baseline-rendered.png",
        )

        shutil.copyfile(
            verified["candidate_path"],
            evidence/"admitted-candidate.png",
        )

        shutil.copyfile(
            verified["review_path"],
            evidence/"PLATE_REVIEW.json",
        )

        shutil.copyfile(
            verified["record_path"],
            evidence/"PLATE_ADMISSION.json",
        )

        candidate_bytes=verified[
            "candidate_path"
        ].read_bytes()

        plate.write_bytes(
            candidate_bytes
        )

        admitted_sha=digest(
            plate.read_bytes()
        )

        if admitted_sha != record["candidate"]["sha256"]:
            raise ValueError(
                f"{key}: admitted candidate SHA-256 drift."
            )

        baseline_optimization=rendered[key].get(
            "optimization"
        )

        if baseline_optimization is not None:
            rendered[key]["baseline_render_optimization"]=(
                baseline_optimization
            )

        admitted_optimization=dict(
            baseline_optimization or {}
        )

        admitted_optimization.update({
            "selected":"admitted palette-256",
            "selected_bytes":record["candidate"]["bytes"],
            "selected_sha256":record["candidate"]["sha256"],
            "color_space":(
                "indexed Palette-256; locked admitted candidate"
            ),
            "admission_override":True,
        })

        rendered[key]["optimization"]=(
            admitted_optimization
        )

        budget=rendered[key].get(
            "budget_bytes"
        )

        byte_status,byte_utilization=byte_budget_status(
            record["candidate"]["bytes"],
            budget,
        )

        rendered[key]["byte_status"]=byte_status
        rendered[key]["byte_budget_utilization"]=(
            byte_utilization
        )
        rendered[key]["within_budget"]=(
            byte_status != "OVER BUDGET"
        )

        rendered[key]["admission"]={
            "status":"ADMITTED",
            "method_id":record["method"]["method_id"],
            "admission_record_sha256":verified[
                "record_sha256"
            ],
            "authorized_by":record[
                "authorization"
            ]["authorized_by"],
            "baseline_sha256":record[
                "baseline"
            ]["sha256"],
            "admitted_sha256":record[
                "candidate"
            ]["sha256"],
            "candidate_bytes":record[
                "candidate"
            ]["bytes"],
            "whole_page_composition":record[
                "review"
            ]["whole_page_composition"],
        }

        rendered[key]["human_visual_acceptance"]=(
            "graphic PASS via locked admission review"
        )

        rendered[key]["kindle_rendering"]=(
            "locked candidate graphic has Kindle PASS; "
            "this complete build is not separately claimed "
            "as Kindle-tested"
        )

        applied.append({
            "component":key,
            "method_id":record["method"]["method_id"],
            "authorized_by":record[
                "authorization"
            ]["authorized_by"],
            "baseline_sha256":record[
                "baseline"
            ]["sha256"],
            "candidate_sha256":record[
                "candidate"
            ]["sha256"],
            "candidate_bytes":record[
                "candidate"
            ]["bytes"],
            "record_sha256":verified[
                "record_sha256"
            ],
            "evidence_directory":str(
                evidence.relative_to(run_dir)
            ).replace("\\","/"),
        })

    return {
        "schema":APPLIED_SCHEMA,
        "admission_count":len(applied),
        "admissions":applied,
    }
