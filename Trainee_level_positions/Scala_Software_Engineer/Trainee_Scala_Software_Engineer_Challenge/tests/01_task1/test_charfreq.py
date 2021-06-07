from string import ascii_lowercase
from typing import Dict

import pytest
from task1.charfreq import calc_chars_probabilities, count_chars_frequency


@pytest.mark.parametrize('text, result', [
    ('', {}),
    ('_!@#$%^&*()/*-123456789', {}),
    ('test1', {'t': 2, 'e': 1, 's': 1}),
    (ascii_lowercase, {char: 1 for char in ascii_lowercase}),
    ('zzz zzzzzzz zzzz zzzzzzz', {'z': 21}),
    ('Little Dark Age', {'l': 2, 'i': 1, 't': 2, 'e': 2, 'd': 1,
                         'a': 2, 'r': 1, 'k': 1, 'g': 1})
])
def test_frequency_counter(text: str, result: Dict[str, int]):
    assert count_chars_frequency(text) == result


@pytest.mark.parametrize('text, result', [
    ('', {}),
    ('z', {'z': 1.0}),
    ('zcb', {'z': 0.33, 'c': 0.33, 'b': 0.33}),
    ('loovvveeee', {'l': 0.1, 'o': 0.2, 'v': 0.3, 'e': 0.4})
])
def test_probability_calculator(text: str, result: Dict[str, int]):
    assert calc_chars_probabilities(text) == result
