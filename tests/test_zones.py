"""Tests for riskfw.zones -- TRGS 721 zone extent calculation."""

import pytest

from riskfw.exceptions import ZoneCalculationError
from riskfw.zones import (
    ReleaseType,
    VentilationEffectiveness,
    ZoneType,
    analyze_ventilation_effectiveness,
    calculate_zone_extent,
)


def test_should_return_zone_2_with_high_ventilation():
    result = calculate_zone_extent(
        release_rate_kg_s=0.001,
        ventilation_rate_m3_s=5.0,
        substance_name="ethanol",
        release_type="jet",
    )
    assert result.zone_type == ZoneType.ZONE_2
    assert result.radius_m > 0
    assert result.basis_norm == "TRGS 721:2017-09"


def test_should_return_zone_0_with_no_ventilation():
    result = calculate_zone_extent(
        release_rate_kg_s=0.1,
        ventilation_rate_m3_s=0.0,
        substance_name="ethanol",
    )
    assert result.zone_type == ZoneType.ZONE_0
    assert len(result.warnings) > 0


def test_should_return_zone_1_with_medium_ventilation():
    result = calculate_zone_extent(
        release_rate_kg_s=0.1,
        ventilation_rate_m3_s=0.5,
        substance_name="ethanol",
        release_type="jet",
    )
    assert result.zone_type == ZoneType.ZONE_1


def test_should_use_fallback_lel_when_no_substance():
    result = calculate_zone_extent(
        release_rate_kg_s=0.1,
        ventilation_rate_m3_s=2.0,
        lel_percent=2.0,
    )
    assert result.lel_percent == 2.0


def test_should_override_lel_from_substance():
    result = calculate_zone_extent(
        release_rate_kg_s=0.1,
        ventilation_rate_m3_s=2.0,
        substance_name="ethanol",
        lel_percent=99.0,
    )
    assert result.lel_percent == 3.1


def test_should_use_correct_safety_factor_for_pool():
    result = calculate_zone_extent(
        release_rate_kg_s=0.1,
        ventilation_rate_m3_s=2.0,
        release_type="pool",
    )
    assert result.safety_factor == 3.0
    assert result.release_type == ReleaseType.POOL


def test_should_raise_for_negative_release_rate():
    with pytest.raises(ZoneCalculationError):
        calculate_zone_extent(release_rate_kg_s=-1.0, ventilation_rate_m3_s=2.0)


def test_should_raise_for_unknown_release_type():
    with pytest.raises(ZoneCalculationError):
        calculate_zone_extent(
            release_rate_kg_s=0.1,
            ventilation_rate_m3_s=2.0,
            release_type="unknown",
        )


def test_should_warn_when_zone_exceeds_room_volume():
    result = calculate_zone_extent(
        release_rate_kg_s=10.0,
        ventilation_rate_m3_s=0.0,
        room_volume_m3=5.0,
    )
    assert any("exceeds" in w for w in result.warnings)


def test_should_analyze_high_ventilation_effectiveness():
    result = analyze_ventilation_effectiveness(
        room_volume_m3=100.0,
        air_flow_m3_h=1500.0,
        ventilation_type="technisch",
    )
    assert result.effectiveness == VentilationEffectiveness.HIGH
    assert result.can_reduce_zone is True
    assert result.basis_norm == "TRGS 722:2012-08"


def test_should_classify_natural_ventilation_as_variable():
    result = analyze_ventilation_effectiveness(
        room_volume_m3=100.0,
        air_flow_m3_h=500.0,
        ventilation_type="natuerlich",
    )
    assert result.effectiveness == VentilationEffectiveness.VARIABLE
    assert result.can_reduce_zone is False
