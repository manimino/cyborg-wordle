from wordly.word_pool import WordPool


def test_exact_matches():
    guesses = {
        'WONKS': 'WO.KS'
    }
    targets = WordPool()
    targets.apply_guesses(guesses)
    assert targets.pool == set(('WORKS', 'WOCKS'))


def test_non_matches():
    guesses = {
        'GYPSY': '.Y..Y'
    }
    targets = WordPool()
    targets.apply_guesses(guesses)
    assert targets.pool == set(('BYWAY', 'DYKEY', 'MYTHY'))


def test_inexact_matches():
    guesses = {
        'SWORD': '?????'
    }
    targets = WordPool()
    targets.apply_guesses(guesses)
    assert targets.pool == set(('WORDS',))


def test_two_inexact_matches_same_letter():
    guesses = {
        'CHESS': '...??'
    }
    targets = WordPool()
    targets.apply_guesses(guesses)
    assert targets.pool == set(['SISAL', 'ASSAM', 'SISTA', 'ASSAI', 'OSSIA', 'SASIN', 'SYSOP', 'ASSAY', 'ASSOT'])


def test_several_guesses():
    guesses = {
        'WEARY': 'W..?.',
        'BLIND': '...N.',
    }
    targets = WordPool()
    targets.apply_guesses(guesses)
    assert targets.pool == set(('WRONG','WRUNG'))


def test_several_more_guesses():
    guesses = {
        'CLOCK': '.....',
        'ROUST': '?.U..',
        'NUMBS': '??...',
        'QUEEN': '.?..?',
    }
    targets = WordPool()
    targets.apply_guesses(guesses)
    assert targets.pool == set(['WRUNG', 'GRUND', 'ANURA', 'PRUNE', 'INURE'])


def test_adverse():
    # Trying a test against Absurdle (Adversarial Wordle)
    # Got it in six guesses, respectable. Esp since we're sorting by frequency and not min tree size.
    guesses = {
        'AUDIO': '?....',
        'BLACK': '..?..',
        'GAMES': '.A...',
        'PARTY': '.A..Y',
        'FAWNY': '.A..Y',
    }
    targets = WordPool()
    targets.apply_guesses(guesses)
    assert targets.pool == set(['JAZZY'])


def test_adverse_again():
    # Trying a test against Absurdle (Adversarial Wordle)
    # Got it in six guesses, respectable. Esp since we're sorting by frequency and not min tree size.
    guesses = {
        'FROND': '.....',
        'ITEMS': '..?..',
        'BELAH': '.?.?.',
        'CAKEY': '.A.?.'
    }
    targets = WordPool()
    targets.apply_guesses(guesses)
    assert targets.pool == set(['VAGUE', 'GAUZE', 'GAUJE', 'GAUGE'])
