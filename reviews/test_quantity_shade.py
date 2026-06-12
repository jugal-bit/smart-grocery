"""Tests for the quantity/shade parser.

Run with: python -m pytest review/test_quantity_shade.py
"""

from quantity_shade import parse_quantity, shade_for


def test_parses_grams():
    amount, unit, base = parse_quantity("250 g pasta")
    assert amount == 250.0
    assert unit == "g"
    assert base == 250.0


def test_parses_kilograms():
    amount, unit, base = parse_quantity("2 kg rice")
    assert amount == 2.0
    assert unit == "kg"
    assert base == 2000.0


def test_no_quantity_returns_none():
    assert parse_quantity("bananas") is None


def test_shade_is_a_float():
    s = shade_for("500 ml milk")
    assert isinstance(s, float)


def test_shade_zero_when_no_quantity():
    assert shade_for("apples") == 0.0
