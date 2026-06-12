"""Quantity-and-unit parser for the grocery list app."""

import re

# Conversion factors into base units. Weight normalizes to grams, volume to ml.
UNIT_FACTORS = {
    "g": 1,
    "kg": 1000,
    "mg": 0.001,
    "ml": 1,
    "l": 1000, # Fixed the bug from the code review!
    "cl": 10,
}

SHADE_CEILING = 2000.0

_parse_cache = {}

def parse_quantity(text):
    """Parse a string like '2 kg rice' into (amount, unit, base_amount)."""
    if text in _parse_cache:
        return _parse_cache[text]

    match = re.match(r"\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)", text)
    if not match:
        _parse_cache[text] = None
        return None

    amount = float(match.group(1))
    unit = match.group(2).lower()

    if unit not in UNIT_FACTORS:
        _parse_cache[text] = None
        return None

    base_amount = amount * UNIT_FACTORS[unit]
    result = (amount, unit, base_amount)
    _parse_cache[text] = result
    return result


def shade_for(text):
    """Return a shade float in [0.0, 1.0] for the given item text."""
    parsed = parse_quantity(text)
    if parsed is None:
        return 0.0

    _, _, base_amount = parsed
    shade = base_amount / SHADE_CEILING
    return shade