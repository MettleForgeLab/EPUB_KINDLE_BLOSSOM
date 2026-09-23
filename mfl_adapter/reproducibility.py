"""Build reproducibility evidence.

The adapter can prove byte identity between two generated EPUBs and
records the runtime boundary within which reproducibility was tested.

Cross-runtime or cross-platform byte identity is not silently claimed.
"""
from __future__ import annotations

import importlib.metadata
import platform
from pathlib import Path
import sys
from typing import Any
import zipfile
import zlib

from .core import digest


ZIP_METADATA_FIELDS = (
    "filename",
    "date_time",
    "compress_type",
    "create_system",
    "external_attr",
    "flag_bits",
    "CRC",
    "file_size",
    "compress_size",
    "extra",
    "comment",
)


def _package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def runtime_fingerprint(
    rendering: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result={
        "schema":"mfl.runtime-fingerprint/1",
        "python":{
            "implementation":platform.python_implementation(),
            "version":platform.python_version(),
        },
        "platform":{
            "system":platform.system(),
            "release":platform.release(),
            "machine":platform.machine(),
        },
        "zlib":{
            "compiled_version":zlib.ZLIB_VERSION,
            "runtime_version":zlib.ZLIB_RUNTIME_VERSION,
        },
        "packages":{
            "Pillow":_package_version("Pillow"),
            "playwright":_package_version("playwright"),
            "lxml":_package_version("lxml"),
        },
    }

    if rendering:
        result["renderer"]={
            "browser":rendering.get("browser"),
            "platform":rendering.get("platform"),
            "runtime_versions":rendering.get(
                "runtime_versions",
                {},
            ),
        }

    return result


def packaging_evidence(
    epub: str | Path,
) -> dict[str, Any]:
    epub=Path(epub).resolve()

    if not epub.is_file():
        raise FileNotFoundError(epub)

    with zipfile.ZipFile(epub) as archive:
        infos=archive.infolist()

        first=infos[0] if infos else None

        timestamps=sorted({
            tuple(info.date_time)
            for info in infos
        })

        create_systems=sorted({
            info.create_system
            for info in infos
        })

        compression_types=sorted({
            info.compress_type
            for info in infos
        })

        return {
            "epub_sha256":digest(epub.read_bytes()),
            "bytes":epub.stat().st_size,
            "member_count":len(infos),
            "first_member":(
                first.filename
                if first is not None
                else None
            ),
            "mimetype_first":(
                first is not None
                and first.filename == "mimetype"
            ),
            "mimetype_stored":(
                first is not None
                and first.filename == "mimetype"
                and first.compress_type == zipfile.ZIP_STORED
            ),
            "timestamps":[
                list(value)
                for value in timestamps
            ],
            "create_systems":create_systems,
            "compression_types":compression_types,
            "archive_comment_bytes":len(archive.comment),
        }


def compare_epubs(
    first: str | Path,
    second: str | Path,
) -> dict[str, Any]:
    first=Path(first).resolve()
    second=Path(second).resolve()

    for path in (first,second):
        if not path.is_file():
            raise FileNotFoundError(path)

    first_bytes=first.read_bytes()
    second_bytes=second.read_bytes()

    with (
        zipfile.ZipFile(first) as a,
        zipfile.ZipFile(second) as b,
    ):
        ai=a.infolist()
        bi=b.infolist()

        a_names=[item.filename for item in ai]
        b_names=[item.filename for item in bi]

        a_set=set(a_names)
        b_set=set(b_names)

        added=sorted(b_set-a_set)
        removed=sorted(a_set-b_set)

        payload_differences=[]

        for name in sorted(a_set & b_set):
            if digest(a.read(name)) != digest(b.read(name)):
                payload_differences.append(name)

        metadata_differences=[]

        for left,right in zip(ai,bi):
            if left.filename != right.filename:
                continue

            differences={}

            for field in ZIP_METADATA_FIELDS:
                lv=getattr(left,field)
                rv=getattr(right,field)

                if lv != rv:
                    differences[field]={
                        "first":repr(lv),
                        "second":repr(rv),
                    }

            if differences:
                metadata_differences.append({
                    "member":left.filename,
                    "fields":differences,
                })

        member_order_identical=(a_names == b_names)
        payloads_identical=(
            not added
            and not removed
            and not payload_differences
        )

        zip_metadata_identical=(
            member_order_identical
            and not metadata_differences
            and a.comment == b.comment
        )

    byte_identical=(first_bytes == second_bytes)

    if byte_identical:
        status="PASS"
    elif not payloads_identical:
        status="PAYLOAD DIFFERENCE"
    elif not zip_metadata_identical:
        status="CONTAINER DIFFERENCE"
    else:
        status="ENCODING DIFFERENCE"

    return {
        "schema":"mfl.epub-reproducibility-comparison/1",
        "status":status,
        "byte_identical":byte_identical,
        "first":{
            "path":str(first),
            "sha256":digest(first_bytes),
            "bytes":len(first_bytes),
        },
        "second":{
            "path":str(second),
            "sha256":digest(second_bytes),
            "bytes":len(second_bytes),
        },
        "member_order_identical":member_order_identical,
        "member_payloads_identical":payloads_identical,
        "zip_metadata_identical":zip_metadata_identical,
        "added_members":added,
        "removed_members":removed,
        "payload_differences":payload_differences,
        "metadata_differences":metadata_differences,
    }


def reproducibility_record(
    epub: str | Path,
    *,
    rendering: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema":"mfl.reproducibility-record/1",
        "publication":packaging_evidence(epub),
        "runtime":runtime_fingerprint(rendering),
        "claim_scope":{
            "same_recorded_runtime":(
                "Byte-identical reproducibility is tested within "
                "the recorded runtime/toolchain."
            ),
            "cross_runtime":(
                "Cross-runtime and cross-platform byte identity "
                "are not claimed without separate evidence."
            ),
        },
    }
