from mfl_adapter.device_profiles import (
    MFL_RESERVE_RATIO,
    coverage_status,
    get_device_profile,
    plan_plate,
    plan_plate_for_device,
)


def test_current_kindle_reference_dimensions():
    assert get_device_profile("paperwhite-5").width_px == 1236
    assert get_device_profile("paperwhite-6").width_px == 1272
    assert get_device_profile("colorsoft").width_px == 1272
    assert get_device_profile("scribe-1-2").width_px == 1860
    assert get_device_profile("scribe-3").width_px == 1986


def test_mfl_reserve_policy_is_separate_from_device_data():
    assert MFL_RESERVE_RATIO == 1.25


def test_coverage_status_thresholds():
    assert coverage_status(1.30) == "RESERVE MET"
    assert coverage_status(1.10) == "NATIVE COVERAGE"
    assert coverage_status(0.99) == "UNDER-RESOLVED"


def test_jules_gravity_has_reserve_on_paperwhite_6():
    plan=plan_plate_for_device(
        source_width_px=2000,
        source_height_px=1500,
        display_fraction=0.72,
        device_key="paperwhite-6",
    )

    assert plan["status"] == "RESERVE MET"
    assert plan["planning_basis"]["css_viewport_claim"] is False
    assert round(plan["estimated_demand"]["width_px"],2) == 915.84
    assert plan["coverage_ratio"] > 2.18


def test_jules_gravity_has_reserve_on_scribe_3():
    plan=plan_plate_for_device(
        source_width_px=2000,
        source_height_px=1500,
        display_fraction=0.72,
        device_key="scribe-3",
    )

    assert plan["status"] == "RESERVE MET"
    assert round(plan["estimated_demand"]["width_px"],2) == 1429.92
    assert plan["coverage_ratio"] > 1.39


def test_underresolved_plate_is_reported():
    plan=plan_plate_for_device(
        source_width_px=800,
        source_height_px=600,
        display_fraction=0.90,
        device_key="scribe-3",
    )

    assert plan["status"] == "UNDER-RESOLVED"


def test_multi_device_plan_reports_required_width():
    plan=plan_plate(
        source_width_px=2000,
        source_height_px=1500,
        display_fraction=0.72,
        device_keys=(
            "paperwhite-6",
            "colorsoft",
            "scribe-3",
        ),
    )

    assert plan["worst_status"] == "RESERVE MET"
    assert (
        plan["minimum_source_width_for_all_devices_px"]
        == 1788
    )
