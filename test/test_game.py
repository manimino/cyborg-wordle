import pytest

from wordly.game import Game, ERR_NON_WORD, ERR_HARD_MODE, ERR_NON_5_LETTER


@pytest.mark.parametrize('word,err_str', [
    ('XXXXX', ERR_NON_WORD.format('XXXXX')),
    ('SNARES', ERR_NON_5_LETTER),
    ('GUESS', '')
])
def test_guess_non_word(word, err_str):
    g = Game()
    assert g.guess_word(word) == err_str


def test_hard_mode_reject():
    g = Game(hard_mode=True)
    g.target = 'ZIPPY'
    r1 = g.guess_word('HAPPY')
    r2 = g.guess_word('PARTY')
    assert r1 == ''
    assert r2 == ERR_HARD_MODE.format('PARTY')


def test_hard_mode_success():
    g = Game(hard_mode=True)
    g.target = 'SOLID'
    r1 = g.guess_word('WASHY')
    r2 = g.guess_word('SCARE')
    r3 = g.guess_word('SOLVE')
    r4 = g.guess_word('SOLID')
    print(g.guesses)
    if any([r1, r2, r3, r4]):
        assert False, f'expected empty, but got: "{r1} {r2} {r3} {r4}"'
