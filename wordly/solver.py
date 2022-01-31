import copy

from wordly.game import make_guess
from wordly.word_pool import WordPool
from wordly.word_list import all_wordle_words

"""
The Solver applies guesses to a Dictionary, whittling down its available word set. 
"""
class Solver():
    def __init__(self, hard_mode=False):
        self.hard_mode = hard_mode
        # targets represents the remaining possible solutions to a puzzle after applying guesses
        self.targets = WordPool()
        # "valids" contains the words that can be guessed. In Easy Mode, "valids" is the
        # whole Wordle dictionary; in Hard Mode it is a subset of that.
        self.valids = WordPool()
        self.freqs = {}
        for word, freq in all_wordle_words:
            self.freqs[word] = freq

    def get_next_words(self, guesses):
        # Try each combination of (valid word, target)
        # Find the one that most likely constrains the target pool to very few / very common words
        self.targets.apply_guesses(guesses)
        if self.hard_mode:
            self.valids.apply_hardmode_constraints(guesses)

        guess_scores = []
        i = 0
        #print('searching {} * {}'.format(len(self.valids.pool), len(self.targets.pool)))
        for guess in self.valids.pool:
            i += 1
            if i % 1000 == 0:
                print(round(i*100 / len(self.valids.pool), 2), '% done')
            guess_score = 0
            guesses_copy = copy.deepcopy(guesses)
            for tw in self.targets.pool:
                targets_copy = copy.deepcopy(self.targets)
                guesses_copy[guess] = make_guess(guess, tw)
                targets_copy.apply_guesses(guesses_copy)
                guess_score += len(targets_copy.pool)
            guess_scores.append((guess, guess_score))
        guess_scores.sort(key=lambda x: x[1])
        return guess_scores

"""
Functions that use the Solver and its Dictionary
"""
def sanitize_validate_input(guesses:dict) -> dict:
    guesses_upper = {}
    for guess, result in guesses.items():
        guesses_upper[guess.upper()] = result.upper()
        assert len(guess) == 5
        assert len(result) == 5
        assert guess.isalpha()
        for c in result:
            assert c.isalpha() or c in ['.', '?']
    return guesses_upper


def recommend_next_words(guesses: dict, hard_mode=False) -> list:
    guesses = sanitize_validate_input(guesses)
    # run solver
    s = Solver(hard_mode)
    next_words = s.get_next_words(guesses)
    if len(next_words) > 10:
        return next_words[:10]
    else:
        return next_words
