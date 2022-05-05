import pytest

from wordly.guess import guess_result


@pytest.mark.parametrize("word, response", [
    ('FOOLS', 'FOOLS'),  # whole word matches
    ('COOLS', '.OOLS'),  # many exact matches
    ('OOOOO', '.OO..'),  # two exact matches
    ('OXXOO', '?..?.'),  # two inexact matches
    ('OBOES', '?.O.S'),  # one inexact match, then one exact match
    ('XXOOX', '..O?.'),  # one exact match, then one inexact match
])
def test_guess_response(word, response):
    target = 'FOOLS'
    assert guess_result(word, target) == response

