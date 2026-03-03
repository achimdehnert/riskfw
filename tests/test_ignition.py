"""Tests for riskfw.ignition -- EN 1127-1:2019 ignition source assessment."""

import pytest

from riskfw.ignition import IgnitionRisk, IgnitionSourceMatrix


@pytest.fixture
def matrix() -> IgnitionSourceMatrix:
    return IgnitionSourceMatrix()


def test_should_return_none_risk_when_source_not_present(matrix):
    result = matrix.assess("S01", is_present=False, is_effective=False)
    assert result.risk_level == IgnitionRisk.NONE


def test_should_return_high_risk_when_effective_without_mitigation(matrix):
    result = matrix.assess("S04", is_present=True, is_effective=True, mitigation="")
    assert result.risk_level == IgnitionRisk.HIGH


def test_should_return_low_risk_when_mitigated(matrix):
    result = matrix.assess("S04", is_present=True, is_effective=True, mitigation="Ex-Anlage")
    assert result.risk_level == IgnitionRisk.LOW


def test_should_return_low_risk_when_present_but_not_effective(matrix):
    result = matrix.assess("S01", is_present=True, is_effective=False)
    assert result.risk_level == IgnitionRisk.LOW


def test_should_raise_for_unknown_source_id(matrix):
    with pytest.raises(ValueError):
        matrix.assess("S99", is_present=True, is_effective=True)


def test_should_have_all_13_sources(matrix):
    assert len(matrix.all_sources) == 13


def test_should_have_correct_source_names(matrix):
    assert "Oberflaechen" in matrix.all_sources["S01"]["name"]
    assert "Reaktionen" in matrix.all_sources["S13"]["name"]


def test_should_include_norm_reference(matrix):
    result = matrix.assess("S06", is_present=True, is_effective=False)
    assert result.norm_reference == "EN 1127-1:2019"
    assert "6.6" in result.norm_clause


def test_should_assess_all_sources_batch(matrix):
    data = [
        {"source_id": "S01", "is_present": True, "is_effective": False},
        {"source_id": "S04", "is_present": True, "is_effective": True, "mitigation": "Ex-Anlage"},
        {"source_id": "S07", "is_present": False, "is_effective": False},
    ]
    results = matrix.assess_all(data)
    assert len(results) == 3
    assert results[2].risk_level == IgnitionRisk.NONE
