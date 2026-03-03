"""Tests for riskfw.substances."""

import pytest

from riskfw.exceptions import SubstanceNotFoundError
from riskfw.substances import fuzzy_lookup, get_substance_properties, list_substances
from riskfw.substances.database import SUBSTANCE_DATABASE


def test_should_return_exact_match():
    result = get_substance_properties("ethanol")
    assert result.name == "Ethanol"
    assert result.lower_explosion_limit == 3.1
    assert result.cas_number == "64-17-5"


def test_should_resolve_english_alias():
    result = get_substance_properties("hydrogen")
    assert result.name == "Wasserstoff"


def test_should_resolve_ipa_alias():
    result = get_substance_properties("ipa")
    assert result.name == "Isopropanol (2-Propanol)"


def test_should_be_case_insensitive():
    result = get_substance_properties("ETHANOL")
    assert result.name == "Ethanol"


def test_should_raise_for_unknown_substance():
    with pytest.raises(SubstanceNotFoundError):
        get_substance_properties("unbekannter_stoff_xyz")


def test_should_return_fuzzy_match_for_close_name():
    match = fuzzy_lookup("etanol")
    assert match == "ethanol"


def test_should_return_none_for_no_fuzzy_match():
    match = fuzzy_lookup("xyz_unbekannt_123")
    assert match is None


def test_should_list_all_substances():
    substances = list_substances()
    assert len(substances) == len(SUBSTANCE_DATABASE)
    assert any(s.name == "Ethanol" for s in substances)


def test_should_have_correct_explosion_groups():
    h2 = get_substance_properties("wasserstoff")
    assert h2.explosion_group == "IIC"
    ethanol = get_substance_properties("ethanol")
    assert ethanol.explosion_group == "IIB"


def test_should_have_lel_values_for_all_substances():
    for substance in list_substances():
        assert substance.lower_explosion_limit > 0, f"{substance.name} has LEL=0"
