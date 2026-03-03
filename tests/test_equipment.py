"""Tests for riskfw.equipment -- ATEX suitability checks."""

import pytest

from riskfw.equipment import check_equipment_suitability
from riskfw.exceptions import ATEXCheckError


def test_should_approve_2g_for_zone_1():
    result = check_equipment_suitability("II 2G Ex d IIB T4", "1")
    assert result.is_suitable is True
    assert result.detected_category == "2G"
    assert result.detected_temp_class == "T4"
    assert result.detected_exp_group == "IIB"


def test_should_approve_1g_for_zone_0():
    result = check_equipment_suitability("II 1G Ex ia IIC T6", "0")
    assert result.is_suitable is True
    assert result.detected_category == "1G"


def test_should_reject_3g_for_zone_1():
    result = check_equipment_suitability("II 3G Ex ec IIA T3", "1")
    assert result.is_suitable is False
    assert len(result.issues) > 0


def test_should_reject_when_no_category_in_marking():
    result = check_equipment_suitability("II Ex d IIB T4", "1")
    assert result.is_suitable is False
    assert len(result.issues) > 0


def test_should_normalize_zone_prefix():
    result = check_equipment_suitability("II 2G Ex d IIB T4", "Zone 1")
    assert result.is_suitable is True
    assert result.target_zone == "1"


def test_should_handle_dust_zone_21():
    result = check_equipment_suitability("II 2D Ex tb IIIB T135", "21")
    assert result.detected_category == "2D"
    assert result.is_suitable is True


def test_should_raise_for_unknown_zone():
    with pytest.raises(ATEXCheckError):
        check_equipment_suitability("II 2G Ex d IIB T4", "99")


def test_should_have_correct_basis_norm():
    result = check_equipment_suitability("II 2G Ex d IIB T4", "1")
    assert result.basis_norm == "ATEX 2014/34/EU"
