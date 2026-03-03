"""Tests for riskfw.reports."""

from riskfw.ignition.models import IgnitionAssessment, IgnitionRisk
from riskfw.reports import IgnitionAssessmentReport, ZoneCalculationReport


def test_should_create_zone_calculation_report():
    report = ZoneCalculationReport(
        project_name="Testanlage",
        zone_name="Zone Fuellstation",
        substance_name="Ethanol",
        substance_lel=3.1,
        release_rate_kg_s=0.1,
        ventilation_rate_m3_s=2.0,
        release_type="jet",
        zone_type="1",
        radius_m=2.3,
        volume_m3=50.9,
        dilution_factor=19.9,
        safety_factor=5.0,
        basis_norm="TRGS 721:2017-09",
        riskfw_version="0.1.0",
    )
    assert report.project_name == "Testanlage"
    assert report.basis_norm == "TRGS 721:2017-09"
    assert report.warnings == []


def test_should_detect_unmitigated_high_risk():
    assessments = [
        IgnitionAssessment(
            source_id="S04", source_name="Elektrische Anlagen",
            is_present=True, is_effective=True,
            risk_level=IgnitionRisk.HIGH, mitigation="",
        ),
    ]
    report = IgnitionAssessmentReport(
        project_name="Test", zone_type="1", assessments=assessments
    )
    assert report.has_unmitigated_high_risk is True
    assert len(report.high_risk_sources) == 1


def test_should_not_flag_mitigated_risk():
    assessments = [
        IgnitionAssessment(
            source_id="S04", source_name="Elektrische Anlagen",
            is_present=True, is_effective=True,
            risk_level=IgnitionRisk.LOW, mitigation="Ex-Schutz installiert",
        ),
    ]
    report = IgnitionAssessmentReport(
        project_name="Test", zone_type="1", assessments=assessments
    )
    assert report.has_unmitigated_high_risk is False


def test_should_group_sources_by_risk():
    assessments = [
        IgnitionAssessment("S01", "Heisse Oberflaechen", True, True, IgnitionRisk.HIGH),
        IgnitionAssessment("S04", "Elektrische Anlagen", True, False, IgnitionRisk.LOW),
        IgnitionAssessment("S07", "Blitzschlag", False, False, IgnitionRisk.NONE),
    ]
    report = IgnitionAssessmentReport("Test", "1", assessments)
    groups = report.sources_by_risk
    assert len(groups["high"]) == 1
    assert len(groups["low"]) == 1
    assert len(groups["none"]) == 1
