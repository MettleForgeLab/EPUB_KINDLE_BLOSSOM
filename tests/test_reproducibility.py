from __future__ import annotations

import json

from mfl_adapter.core import write_epub
from mfl_adapter.reproducibility import (
    compare_epubs,
    packaging_evidence,
    reproducibility_record,
    runtime_fingerprint,
)


def members(text=b"same"):
    return {
        "mimetype":b"application/epub+zip",
        "META-INF/container.xml":b"<container/>",
        "OEBPS/test.txt":text,
    }


def test_runtime_fingerprint_records_compression_boundary():
    result=runtime_fingerprint()

    assert result["python"]["version"]
    assert result["zlib"]["compiled_version"]
    assert result["zlib"]["runtime_version"]
    assert result["packages"]["Pillow"]


def test_packaging_evidence_records_epub_contract(tmp_path):
    epub=tmp_path/"book.epub"
    write_epub(epub,members())

    result=packaging_evidence(epub)

    assert result["first_member"] == "mimetype"
    assert result["mimetype_first"] is True
    assert result["mimetype_stored"] is True
    assert result["member_count"] == 3


def test_compare_identical_epubs_passes(tmp_path):
    first=tmp_path/"first.epub"
    second=tmp_path/"second.epub"

    write_epub(first,members())
    write_epub(second,members())

    result=compare_epubs(first,second)

    assert result["status"] == "PASS"
    assert result["byte_identical"] is True
    assert result["member_payloads_identical"] is True
    assert result["zip_metadata_identical"] is True


def test_compare_detects_payload_difference(tmp_path):
    first=tmp_path/"first.epub"
    second=tmp_path/"second.epub"

    write_epub(first,members(b"first"))
    write_epub(second,members(b"second"))

    result=compare_epubs(first,second)

    assert result["status"] == "PAYLOAD DIFFERENCE"
    assert result["byte_identical"] is False
    assert result["payload_differences"] == [
        "OEBPS/test.txt"
    ]


def test_reproducibility_record_does_not_claim_cross_runtime(tmp_path):
    epub=tmp_path/"book.epub"
    write_epub(epub,members())

    result=reproducibility_record(epub)

    assert result["publication"]["mimetype_stored"] is True
    assert "not claimed" in (
        result["claim_scope"]["cross_runtime"].lower()
    )
