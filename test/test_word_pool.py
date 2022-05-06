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


@pytest.mark.parametrize("words, est_entropy", [
    ({'SPIKE'}, 0),
    ({'ABATE', 'OOZES'}, 1),
    ({'ABATE', 'OOZES', 'CANDY'}, 1),
    ({'AAAAA', 'BBBBB', 'CCCCC'}, 1),
    ({'BBBBA', 'BBBAB', 'BBABB', 'BABBB', 'ABBBB'}, 0.722),  # mostly B, so entropy is lower than 1.
    ({'KECKS', 'MECKS', 'FECKS', 'HECKS'}, 0.4)
])
def test_entropy(words, est_entropy):
    # Set up a word pool with our fake test words. Manually create the pos_counts.
    wp = WordPool()
    wp.pool = words
    wp.pos_counts = []
    for i in range(5):
        wp.pos_counts.append(Counter([w[i] for w in wp.pool]))
    assert abs(sum(wp.get_entropy())/5 - est_entropy) < 0.01, f'entropy off for: {words}'

