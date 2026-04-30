# riskfw — Risk Framework

Pure-Python safety calculation library for explosion protection.
No Django, no HTTP, no external dependencies — stdlib only.

[![PyPI](https://img.shields.io/pypi/v/riskfw)](https://pypi.org/project/riskfw/)
[![Python](https://img.shields.io/pypi/pyversions/riskfw)](https://pypi.org/project/riskfw/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Standards

| Module | Standard |
|---|---|
| `riskfw.zones` | TRGS 721:2017-09, TRGS 722:2012-08 |
| `riskfw.equipment` | ATEX 2014/34/EU, IEC 60079-0 |
| `riskfw.ignition` | EN 1127-1:2019 |
| `riskfw.substances` | GESTIS/DGUV (static, auditable) |

## Installation

```bash
pip install riskfw
```

Or as Git dependency (pre-release):

```
riskfw @ git+https://github.com/achimdehnert/riskfw@v0.1.0
```

## Quick Start

```python
from riskfw.zones import calculate_zone_extent
from riskfw.equipment import check_equipment_suitability
from riskfw.substances import get_substance_properties

# Zone calculation per TRGS 721
result = calculate_zone_extent(
    release_rate_kg_s=0.1,
    ventilation_rate_m3_s=2.0,
    substance_name="ethanol",
    release_type="jet",
)
print(result.zone_type)   # ZoneType.ZONE_1
print(result.radius_m)

# ATEX equipment check
check = check_equipment_suitability(ex_marking="II 2G Ex d IIB T4", zone="1")
print(check.is_suitable)  # True

# Substance lookup
props = get_substance_properties("ethanol")
print(props.lower_explosion_limit)  # 3.1
```

## Versioning

- `MAJOR`: Norm edition changes affecting calculation results
- `MINOR`: New norm support added
- `PATCH`: Bugfix or new substances without normative impact

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT
