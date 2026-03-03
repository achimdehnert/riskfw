# Changelog

## [0.1.0] — 2026-03-03

### Added
- `riskfw.substances`: GESTIS-based substance database (13 substances), fuzzy lookup via stdlib `difflib`
- `riskfw.zones`: Zone extent calculation per TRGS 721:2017-09, ventilation analysis per TRGS 722:2012-08
- `riskfw.equipment`: ATEX equipment suitability check per ATEX 2014/34/EU
- `riskfw.ignition`: Ignition source assessment matrix per EN 1127-1:2019 (all 13 sources)
- `riskfw.reports`: `ZoneCalculationReport`, `IgnitionAssessmentReport` dataclasses
- `riskfw.constants`: Norm version constants
- `riskfw.exceptions`: `SubstanceNotFoundError`, `ZoneCalculationError`, `ATEXCheckError`
- Migrated from `risk-hub/explosionsschutz/calculations.py`

### Substances (GESTIS, Stand 2026-03-01, Prüfung fällig 2027-03-01)
- Aceton, Ethanol, Methanol, Toluol, Xylol, Benzin, Diesel
- Wasserstoff, Methan, Propan, Isopropanol, Butanol, Ethylacetat
