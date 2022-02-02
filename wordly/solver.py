import copy
import random

from wordly.game import make_guess
from wordly.util import ALL_POSSIBLE_RESULTS
from wordly.word_pool import WordPool
from wordly.word_list import all_wordle_words

"""
The Solver suggests a next word based on all available information.

An optimal solver would generate a full possibility tree for all possible target words
and all available guesses. It minimizes the depth of the search tree. 
That would take days to run on a modern computer, even in a compiled language. [1]

So this solver relies on various heuristics to short-cut the process. 
Heuristics have near-optimal performance in practice [2].

As a human player, these strategies intuitive.
- Guess words that contain letters we haven't seen yet to maximize information gain.
- 

[1] https://www.poirrier.ca/notes/wordle/
[2] http://sonorouschocolate.com/notes/index.php?title=The_best_strategies_for_Wordle
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
        best_score = float('inf')
        guess_pool = random.sample(list(self.valids.pool), min(len(self.valids.pool), 25))
        targets_pool = list(self.targets.pool)
        """
        if len(self.targets.pool) > 243:  # 3^5
            # If there are many targets, we can simply try all guess results.
            # There are 3^5 of those (each letter has 3 possible outcomes).
            for guess in guess_pool:
                guess_score = 0
                for result in ALL_POSSIBLE_RESULTS:
                    rstr = ''.join([guess[i] if result[i] == '*'
                                    else result[i]
                                    for i in range(len(result))])
                    new_guesses = {guess:rstr}
                    new_guesses.update(guesses)
                    targets_copy = copy.deepcopy(self.targets)
                    targets_copy.apply_guesses(new_guesses)
                    guess_score += len(targets_copy.pool)
                    if guess_score > best_score:
                        break
                if 0 < guess_score < best_score:
                    best_score = guess_score
                    guess_scores.append((guess, guess_score))
        else:
        """
        for guess in guess_pool:
            guess_score = 0
            guesses_copy = copy.deepcopy(guesses)
            random.shuffle(targets_pool)
            for tw in targets_pool[:25]:
                targets_copy = copy.deepcopy(self.targets)
                new_guesses = {guess: make_guess(guess, tw)}
                new_guesses.update(guesses)
                targets_copy.apply_guesses(guesses_copy)
                guess_score += len(targets_copy.pool)
                if guess_score > best_score:
                    break
            if guess_score < best_score:
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
