"""Whole-publication, policy-aware EPUB audit.

This module is read-only. It verifies exact publication identity, package
structure, navigation, references, platform-specific invariants, and selected
asset identities. It does not render, rebuild, repair, or publish an EPUB.
"""
from __future__ import annotations

from datetime import datetime, timezone
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
from typing import Any

from PIL import Image
from lxml import etree as E

from .core import (
    AdapterError,
    EPUB,
    NS,
    OPF,
    Publication,
    digest,
    package_report,
    require,
    resolve_member,
    text,
)


KNOWN_MEDIA_EXTENSIONS: dict[str, set[str]] = {
    "application/xhtml+xml": {".xhtml", ".html"},
    "text/css": {".css"},
    "image/jpeg": {".jpg", ".jpeg"},
    "image/png": {".png"},
    "image/svg+xml": {".svg"},
    "application/vnd.ms-opentype": {".otf"},
    "font/otf": {".otf"},
    "font/ttf": {".ttf"},
    "application/x-font-ttf": {".ttf"},
    "application/vnd.amazon.ebook": {".azw", ".azw3"},
}

LOCAL_IDREF_ATTRIBUTES = (
    "aria-labelledby",
    "aria-describedby",
    "aria-controls",
    "aria-details",
    "aria-flowto",
    "aria-owns",
    "headers",
)


def _check(
    checks: list[dict[str, Any]],
    check_id: str,
    passed: bool,
    note: str,
    *,
    expected: Any = None,
    actual: Any = None,
) -> None:
    record: dict[str, Any] = {
        "id": check_id,
        "status": "PASS" if passed else "FAIL",
        "note": note,
    }

    if expected is not None:
        record["expected"] = expected

    if actual is not None:
        record["actual"] = actual

    checks.append(record)


def load_publication_policy(
    path: str | Path,
    platform: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load one named platform policy from a publication policy document."""
    path = Path(path).resolve()
    policy = json.loads(path.read_text(encoding="utf-8"))

    require(
        policy.get("schema") == "mfl.publication-audit-policy/1",
        "Unsupported publication-audit policy schema.",
    )

    platforms = policy.get("platforms")

    require(
        isinstance(platforms, dict) and platform in platforms,
        f"Publication policy has no platform named {platform!r}.",
    )

    platform_policy = platforms[platform]

    require(
        isinstance(platform_policy, dict),
        f"Publication policy platform {platform!r} must be an object.",
    )

    return policy, platform_policy


def _manifest_record(pub: Publication) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    items: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}

    for item in pub.opf.xpath("./opf:manifest/opf:item", namespaces=NS):
        item_id = item.get("id")
        href = item.get("href", "")
        member, _ = resolve_member(pub.opf_name, href)

        record = {
            "id": item_id,
            "href": href,
            "member": member,
            "media_type": item.get("media-type"),
            "properties": item.get("properties", "").split(),
        }

        items.append(record)

        if item_id is not None:
            by_id[item_id] = record

    return items, by_id


def _spine_record(
    pub: Publication,
    manifest_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    result = []

    for position, itemref in enumerate(
        pub.opf.xpath("./opf:spine/opf:itemref", namespaces=NS),
        1,
    ):
        item_id = itemref.get("idref")
        manifest = manifest_by_id.get(item_id)

        result.append(
            {
                "position": position,
                "idref": item_id,
                "member": manifest.get("member") if manifest else None,
                "linear": itemref.get("linear", "yes"),
            }
        )

    return result


def _navigation_record(pub: Publication) -> dict[str, Any]:
    toc: list[dict[str, str | None]] = []
    landmarks: list[dict[str, str | None]] = []

    nav_namespaces = dict(NS)
    nav_namespaces["epub"] = EPUB

    for nav_name in pub.nav_names:
        doc = pub.docs[nav_name]

        for anchor in doc.xpath(
            '//x:nav[@epub:type="toc"]//x:a',
            namespaces=nav_namespaces,
        ):
            toc.append(
                {
                    "label": text(anchor),
                    "href": anchor.get("href"),
                    "nav_member": nav_name,
                }
            )

        for anchor in doc.xpath(
            '//x:nav[@epub:type="landmarks"]//x:a',
            namespaces=nav_namespaces,
        ):
            landmarks.append(
                {
                    "label": text(anchor),
                    "href": anchor.get("href"),
                    "type": anchor.get(f"{{{EPUB}}}type"),
                    "nav_member": nav_name,
                }
            )

    return {
        "nav_documents": list(pub.nav_names),
        "toc": toc,
        "landmarks": landmarks,
    }


def _idref_report(pub: Publication) -> dict[str, Any]:
    checked = 0
    failures: list[dict[str, str]] = []

    ids = {
        member: set(doc.xpath('//*[@id]/@id'))
        for member, doc in pub.docs.items()
    }

    for member, doc in pub.docs.items():
        for element in doc.iter():
            if not isinstance(element.tag, str):
                continue

            for attribute in LOCAL_IDREF_ATTRIBUTES:
                value = element.get(attribute)

                if not value:
                    continue

                for target in value.split():
                    checked += 1

                    if target not in ids[member]:
                        failures.append(
                            {
                                "member": member,
                                "attribute": attribute,
                                "target": target,
                            }
                        )

            html_for = element.get("for")

            if html_for:
                checked += 1

                if html_for not in ids[member]:
                    failures.append(
                        {
                            "member": member,
                            "attribute": "for",
                            "target": html_for,
                        }
                    )

    return {
        "checked": checked,
        "failures": failures,
    }


def _logical_text(pub: Publication, member: str) -> str:
    doc = pub.docs.get(member)

    if doc is None:
        return ""

    return text(doc)


def _asset_dimensions(data: bytes) -> list[int] | None:
    try:
        with Image.open(BytesIO(data)) as image:
            return [image.width, image.height]
    except Exception:
        return None


def audit_publication(
    epub: str | Path,
    *,
    expected_sha256: str,
    policy: dict[str, Any] | None = None,
    platform: str | None = None,
    platform_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Audit one exact EPUB against package and optional platform policy."""
    epub = Path(epub).resolve()
    pub = Publication(epub, expected_sha256)
    checks: list[dict[str, Any]] = []

    internal = package_report(pub.members)

    _check(
        checks,
        "package.internal",
        internal.get("status") == "passed",
        "All XHTML resources, fragments, and core accessibility IDREFs resolve.",
        actual=internal,
    )

    manifest, manifest_by_id = _manifest_record(pub)
    spine = _spine_record(pub, manifest_by_id)
    navigation = _navigation_record(pub)
    idrefs = _idref_report(pub)

    manifest_ids = [item["id"] for item in manifest]
    manifest_members = [item["member"] for item in manifest]

    _check(
        checks,
        "manifest.unique_ids",
        len(manifest_ids) == len(set(manifest_ids)),
        "Manifest IDs are unique.",
        actual=len(manifest_ids),
    )

    _check(
        checks,
        "manifest.unique_members",
        len(manifest_members) == len(set(manifest_members)),
        "Manifest hrefs resolve to unique package members.",
        actual=len(manifest_members),
    )

    unresolved_spine = [
        record for record in spine
        if record["member"] is None
    ]

    non_xhtml_spine = [
        record for record in spine
        if record["member"] is not None
        and manifest_by_id[record["idref"]]["media_type"]
        != "application/xhtml+xml"
    ]

    _check(
        checks,
        "spine.resolution",
        not unresolved_spine and not non_xhtml_spine,
        "Every spine idref resolves to an XHTML manifest item.",
        actual={
            "unresolved": unresolved_spine,
            "non_xhtml": non_xhtml_spine,
        },
    )

    media_mismatches = []

    for item in manifest:
        media_type = item["media_type"]
        member = item["member"]

        if media_type not in KNOWN_MEDIA_EXTENSIONS or member is None:
            continue

        suffix = PurePosixPath(member).suffix.lower()

        if suffix not in KNOWN_MEDIA_EXTENSIONS[media_type]:
            media_mismatches.append(
                {
                    "member": member,
                    "media_type": media_type,
                    "suffix": suffix,
                }
            )

    _check(
        checks,
        "manifest.media_extensions",
        not media_mismatches,
        "Known manifest media types match their filename extensions.",
        actual=media_mismatches,
    )

    _check(
        checks,
        "idrefs.extended",
        not idrefs["failures"],
        "Extended local IDREF attributes resolve within their documents.",
        actual=idrefs,
    )

    cover_items = [
        item for item in manifest
        if "cover-image" in item["properties"]
    ]

    _check(
        checks,
        "cover.single_manifest_item",
        len(cover_items) == 1,
        "Exactly one manifest item carries the cover-image property.",
        expected=1,
        actual=len(cover_items),
    )

    if platform_policy is not None:
        expected_name = platform_policy.get("expected_filename")

        if expected_name is not None:
            _check(
                checks,
                "policy.filename",
                epub.name == expected_name,
                "EPUB filename matches the frozen platform policy.",
                expected=expected_name,
                actual=epub.name,
            )

        expected_hash = platform_policy.get("expected_sha256")

        if expected_hash is not None:
            _check(
                checks,
                "policy.sha256",
                pub.sha256 == expected_hash.lower(),
                "EPUB SHA-256 matches the frozen platform policy.",
                expected=expected_hash.lower(),
                actual=pub.sha256,
            )

        expected_bytes = platform_policy.get("expected_bytes")

        if expected_bytes is not None:
            _check(
                checks,
                "policy.bytes",
                epub.stat().st_size == expected_bytes,
                "EPUB byte size matches the frozen platform policy.",
                expected=expected_bytes,
                actual=epub.stat().st_size,
            )

        count_expectations = {
            "members": len(pub.members),
            "manifest_items": len(manifest),
            "spine_documents": len(spine),
        }

        for key, actual in count_expectations.items():
            expected = platform_policy.get(f"expected_{key}")

            if expected is not None:
                _check(
                    checks,
                    f"policy.count.{key}",
                    actual == expected,
                    f"{key.replace('_', ' ').title()} match the platform policy.",
                    expected=expected,
                    actual=actual,
                )

        expected_spine = platform_policy.get("expected_spine")

        if expected_spine is not None:
            actual_spine = [record["member"] for record in spine]

            _check(
                checks,
                "policy.spine",
                actual_spine == expected_spine,
                "Spine order matches the accepted platform architecture.",
                expected=expected_spine,
                actual=actual_spine,
            )

        expected_toc = platform_policy.get("expected_toc")

        if expected_toc is not None:
            actual_toc = [
                {
                    "label": item["label"],
                    "href": item["href"],
                }
                for item in navigation["toc"]
            ]

            _check(
                checks,
                "policy.toc",
                actual_toc == expected_toc,
                "TOC labels and direct destinations match the accepted platform architecture.",
                expected=expected_toc,
                actual=actual_toc,
            )

        expected_landmarks = platform_policy.get("expected_landmarks")

        if expected_landmarks is not None:
            actual_landmarks = [
                {
                    "label": item["label"],
                    "href": item["href"],
                    "type": item["type"],
                }
                for item in navigation["landmarks"]
            ]

            _check(
                checks,
                "policy.landmarks",
                actual_landmarks == expected_landmarks,
                "Landmarks match the accepted platform architecture.",
                expected=expected_landmarks,
                actual=actual_landmarks,
            )

        required_members = platform_policy.get("required_members", [])
        missing_required = [
            member for member in required_members
            if member not in pub.members
        ]

        _check(
            checks,
            "policy.required_members",
            not missing_required,
            "All required platform members are present.",
            actual=missing_required,
        )

        forbidden_members = platform_policy.get("forbidden_members", [])
        present_forbidden = [
            member for member in forbidden_members
            if member in pub.members
        ]

        _check(
            checks,
            "policy.forbidden_members",
            not present_forbidden,
            "No forbidden sibling-platform or stale members are present.",
            actual=present_forbidden,
        )

        forbidden_prefixes = platform_policy.get(
            "forbidden_member_prefixes",
            [],
        )
        present_forbidden_prefixes = {
            prefix: [
                member for member in pub.members
                if member.startswith(prefix)
            ]
            for prefix in forbidden_prefixes
        }
        present_forbidden_prefixes = {
            prefix: members
            for prefix, members in present_forbidden_prefixes.items()
            if members
        }

        _check(
            checks,
            "policy.forbidden_member_prefixes",
            not present_forbidden_prefixes,
            "No forbidden sibling-platform member families are present.",
            actual=present_forbidden_prefixes,
        )

        for prefix, expected_count in platform_policy.get(
            "expected_member_prefix_counts",
            {},
        ).items():
            actual_count = sum(
                member.startswith(prefix)
                for member in pub.members
            )

            _check(
                checks,
                f"policy.member_prefix_count.{prefix}",
                actual_count == expected_count,
                "Package member-family count matches the platform policy.",
                expected=expected_count,
                actual=actual_count,
            )

        assets = []

        for asset in platform_policy.get("required_assets", []):
            member = asset["member"]
            data = pub.members.get(member)

            record = {
                "member": member,
                "present": data is not None,
            }

            if data is not None:
                record.update(
                    {
                        "bytes": len(data),
                        "sha256": digest(data),
                        "dimensions": _asset_dimensions(data),
                    }
                )

            assets.append(record)

            matches = data is not None

            if matches and asset.get("sha256") is not None:
                matches = (
                    digest(data)
                    == asset["sha256"].lower()
                )

            if matches and asset.get("bytes") is not None:
                matches = len(data) == asset["bytes"]

            if matches and asset.get("dimensions") is not None:
                matches = (
                    _asset_dimensions(data)
                    == asset["dimensions"]
                )

            if matches and asset.get("media_type") is not None:
                manifest_matches = [
                    item for item in manifest
                    if item["member"] == member
                ]

                matches = (
                    len(manifest_matches) == 1
                    and manifest_matches[0]["media_type"]
                    == asset["media_type"]
                )

            _check(
                checks,
                f"policy.asset.{member}",
                matches,
                "Required platform asset matches its admitted package identity.",
                expected=asset,
                actual=record,
            )

        for required in platform_policy.get("required_text", []):
            member = required["member"]
            phrase = required["text"]
            expected_count = required.get("count", 1)
            logical = _logical_text(pub, member)
            actual_count = logical.count(phrase)

            _check(
                checks,
                f"policy.required_text.{member}.{len(checks)}",
                actual_count == expected_count,
                "Required reader/source text appears at the expected count.",
                expected={
                    "text": phrase,
                    "count": expected_count,
                },
                actual=actual_count,
            )

        for forbidden in platform_policy.get("forbidden_text", []):
            members = forbidden.get(
                "members",
                list(pub.docs),
            )
            phrase = forbidden["text"]
            occurrences = {}

            for member in members:
                count = _logical_text(pub, member).count(phrase)

                if count:
                    occurrences[member] = count

            _check(
                checks,
                f"policy.forbidden_text.{len(checks)}",
                not occurrences,
                "Forbidden historical, sibling-platform, or production-residue text is absent.",
                expected=phrase,
                actual=occurrences,
            )

        expected_stylesheets = platform_policy.get("expected_stylesheets")

        if expected_stylesheets is not None:
            actual_stylesheets = [
                item["member"]
                for item in manifest
                if item["media_type"] == "text/css"
            ]

            _check(
                checks,
                "policy.stylesheets",
                actual_stylesheets == expected_stylesheets,
                "Shared and platform stylesheet members match the accepted package.",
                expected=expected_stylesheets,
                actual=actual_stylesheets,
            )

    failed = [
        check for check in checks
        if check["status"] == "FAIL"
    ]

    report = {
        "schema": "mfl.publication-audit/1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failed else "FAIL",
        "publication": {
            "path": str(epub),
            "filename": epub.name,
            "sha256": pub.sha256,
            "bytes": epub.stat().st_size,
        },
        "policy": {
            "policy_id": (
                policy.get("policy_id")
                if policy is not None
                else None
            ),
            "platform": platform,
        },
        "package": {
            "opf": pub.opf_name,
            "member_count": len(pub.members),
            "manifest_count": len(manifest),
            "spine": spine,
            "navigation": navigation,
            "cover_items": cover_items,
            "internal": internal,
            "extended_idrefs": idrefs,
        },
        "checks": checks,
        "failure_count": len(failed),
        "failures": failed,
        "mutated_input": False,
        "renderer_review": "NOT INFERRED",
        "human_acceptance": "NOT INFERRED",
    }

    pub.unchanged()

    return report


def write_publication_audit(
    report: dict[str, Any],
    destination: str | Path,
) -> Path:
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    return destination
