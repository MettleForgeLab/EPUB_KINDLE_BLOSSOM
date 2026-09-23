from __future__ import annotations

import json

import pytest

from mfl_adapter.device_profiles import (
    DEVICE_PROFILES,
    get_device_profile,
    plate_pixel_report,
)
from mfl_adapter.tooling import discover_command
from mfl_adapter.validation import (
    new_validation_report,
    write_validation_report,
)


def test_current_device_profiles_are_distinct_and_positive():
    assert len(DEVICE_PROFILES) >= 6

    for profile in DEVICE_PROFILES.values():
        assert profile.width_px > 0
        assert profile.height_px > profile.width_px


def test_paperwhite_6_profile():
    profile = get_device_profile("paperwhite-6")

    assert profile.width_px == 1272
    assert profile.height_px == 1696


def test_scribe_3_profile():
    profile = get_device_profile("scribe-3")

    assert profile.width_px == 1986
    assert profile.height_px == 2648


def test_unknown_device_profile_stops():
    with pytest.raises(KeyError, match="Unknown device profile"):
        get_device_profile("future-kindle-from-mars")


def test_plate_pixel_report_does_not_claim_css_viewport():
    report = plate_pixel_report(
        2560,
        2000,
        "paperwhite-6",
    )

    assert report["covers_device_width"] is True
    assert report["device"]["width_px"] == 1272
    assert "viewport" not in report


def test_explicit_external_tool_discovery(tmp_path):
    fake = tmp_path / "epubcheck.bat"
    fake.write_text("@echo off\n", encoding="utf-8")

    found = discover_command(
        "test",
        ("definitely-not-on-path",),
        explicit=str(fake),
        expected_version="1.2.3",
    )

    assert found.available is True
    assert found.source == "explicit"
    assert found.expected_version == "1.2.3"


def test_missing_external_tool_is_evidence_not_failure():
    found = discover_command(
        "test",
        ("mfl-tool-that-does-not-exist-anywhere",),
    )

    assert found.available is False
    assert found.invocation is None


def test_validation_report_begins_without_silent_pass(
    tmp_path,
):
    epub = tmp_path / "test.epub"
    epub.write_bytes(b"test publication bytes")

    report = new_validation_report(
        epub,
        tmp_path,
    )

    assert report.epubcheck.status == "NOT RUN"
    assert report.ace.status == "NOT RUN"
    assert report.kindle_previewer.status == "NOT RUN"
    assert report.human_acceptance.status == "NOT RUN"

    output = write_validation_report(
        report,
        tmp_path / "VALIDATION_REPORT.json",
    )

    parsed = json.loads(output.read_text(encoding="utf-8"))

    assert parsed["schema"] == "mfl.validation-report/1"
    assert parsed["epub_sha256"] == report.epub_sha256
    assert parsed["human_acceptance"]["status"] == "NOT RUN"
