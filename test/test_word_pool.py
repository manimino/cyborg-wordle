import pytest

from collections import Counter

from wordly.guess import Guess
from wordly.word_pool import WordPool


@pytest.mark.parametrize("guesses, pool", [
    ([Guess('WONKS', 'WO.KS')], {'WORKS', 'WOCKS'}),  # exact matches
    ([Guess('GYPSY', '.Y..Y')], {'BYWAY', 'DYKEY', 'MYTHY'}),  # nonmatches
    ([Guess('SWORD', '?????')], {'WORDS'}),  # inexact matches
    ([Guess('CHESS', '...??')],
     {'SISAL', 'ASSAM', 'SISTA',
      'ASSAI', 'OSSIA', 'SASIN',
      'SYSOP', 'ASSAY', 'ASSOT'}),  # two inexact matches, same letter
    ([Guess('WEARY', 'W..?.'), Guess('BLIND', '...N.')], {'WRONG', 'WRUNG'}),  # two guesses
    ([
        Guess('AUDIO', '?....'),
        Guess('BLACK', '..?..'),
        Guess('GAMES', '.A...'),
        Guess('PARTY', '.A..Y'),
        Guess('FAWNY', '.A..Y'),
    ], {'JAZZY'}),  # test case from an Adversarial Wordle game
    ([
        Guess('CLAST', '...?.'),
        Guess('SPOOR', '?....'),
        Guess('KNEES', '..E.S'),
     ],
     {'QUEYS', 'DIEBS', 'WHEYS',
      'HIEMS', 'VIEWS', 'WHEWS',
      'FIEFS'})  # tests some tricky nonmatch logic
])
def test_guess_pool(guesses, pool):
    targets = WordPool()
    for g in guesses:
        targets.apply_guess(g)
    assert targets.pool == pool

