from collections import Counter
from math import log2
from typing import *

from wordly.guess import Guess
from wordly.word_list import all_wordle_words


"""
A WordPool represents a set of words, with convenience functions for fast lookup and removal.

Initially a word pool contains the whole Wordle dictionary; applying constraints (guesses and results)
will remove words from the pool.

Used by the Solver to represent the set of possible solutions and the set of valid guesses.
"""


class WordPool:

    def __init__(self):
        self.pool = set(w[0] for w in all_wordle_words)  # all available words, initially the entire dictionary.

        # build lookup table of {character: word} to speed up queries
        self.lookup = {}
        for w in self.pool:
            for c in w:
                if c not in self.lookup:
                    self.lookup[c] = set()
                self.lookup[c].add(w)

        # build position counts table, for entropy calcs
        self.pos_counts = []
        for i in range(5):
            self.pos_counts.append(Counter([w[i] for w in self.pool]))

    def remove(self, w: str):
        """Remove a single word from the pool, and update associated data structures."""
        if w not in self.pool:
            return
        self.pool.remove(w)
        for i, c in enumerate(w):
            if w in self.lookup[c]:
                self.lookup[c].remove(w)
            self.pos_counts[i][c] -= 1

    def remove_all_except(self, these: set):
        """Remove all words except for these from the pool."""
        for w in self.pool.difference(these):
            self.remove(w)

    def match_char_pos(self, char: str, pos: int) -> set:
        """Get all words matching a char in a specific position."""
        matches = set()
        for w in self.lookup[char]:
            if w[pos] == char:
                matches.add(w)
        return matches

    def get_entropy(self) -> List[float]:
        """Compute the entropy of each position in the word."""
        ents = []
        n_words = len(self.pool)
        for ct in self.pos_counts:
            pos_entropy = 0
            for v in ct.values():
                if v == n_words or v == 0:
                    # entropy is 0 if all the same, but log would throw an error there
                    continue
                x = v / n_words
                pos_entropy -= x * log2(x)
            ents.append(pos_entropy)
        return ents

    def __str__(self):
        if len(self.pool) <= 10:
            return 'Words remaining: {} {}'.format(len(self.pool), list(self.pool))
        else:
            return 'Words remaining: {} {} ...'.format(len(self.pool), list(self.pool)[:10])

    # -- Guess related functions -- #
    def apply_guess(self, g: Guess):
        """
        Apply guesses to the pool, removing nonmatching words.

        Used when the WordPool represents the set of possible solutions.
        """
        self._apply_exact_matches(g.result)
        self.apply_nonmatches(g.word, g.result)
        self._apply_inexact_matches(g.word, g.result)
        self.remove(g.word)  # prevents guessing the same word repeatedly

    def apply_hardmode_constraints(self, g: Guess):
        """
        Apply guesses / results to the pool, removing words that can't be used in hard mode.

        In hard mode, a word is only usable if it keeps exact and inexact matches from any previous guess.
        Inexact matches are allowed to be in any spot, even the same spot they were in a previous guess;
        only their presence matters. That's a bit different than the _apply_inexact_matches logic.
        """
        # apply greens
        self._apply_exact_matches(g.result)
        # apply yellows
        # first, trim down pool to only words that contain at least one of each yellow letter
        for i, rc in enumerate(g.result):
            if rc == '?':
                c = g.word[i]
                self.remove_all_except(self.lookup[c])

        # now, handle case where there are 2+ yellows / greens of the same letter
        q_counts = Counter(g.word[i] for i in range(len(g.result)) if g.result[i] != '.')
        for w in set(self.pool):  # iterate over copy to avoid modifying iterable
            w_counts = Counter(w)
            for c, count in q_counts.items():
                if w_counts[c] < q_counts[c]:
                    self.remove(w)

    def apply_nonmatches(self, word: str, result: str):
        """Eliminate words from the pool if they contain letters that we know don't match."""
        counts = Counter(word)

        # Cases:
        # - If all copies of a letter are nonmatches, we can eliminate all words containing the letter.
        # - But if there is an inexact or exact match with a different copy of the letter, we
        # can only eliminate words containing too many of the letter and words with the letter
        # at that exact position.
        # Steps:
        # 1. Find nonmatching letters
        # 2. Figure out which case they belong to
        # 3. Apply appropriate filter behavior
        actions = []
        _SKIP = 0
        _NONMATCH_POS = 1
        _NONMATCH_WORD = 2
        for i, ci in enumerate(word):
            if result[i] == '.':
                action = _NONMATCH_WORD
                # check for other occurrences of this char
                for j, cj in enumerate(word):
                    if cj == ci and i != j and result[j] != '.':
                        # found another occurrence, and it's some kind of match
                        action = _NONMATCH_POS
                actions.append(action)
            else:
                actions.append(_SKIP)

        counts = Counter(word)
        for i, ci in enumerate(word):
            if actions[i] == _SKIP:
                continue
            if actions[i] == _NONMATCH_POS:
                # remove word if nonmatch letter is at this pos
                for w in self.match_char_pos(ci, i):
                    self.remove(w)
                # remove word if too many copies of this letter
                for w in list(self.pool):
                    wc = Counter(w)
                    if wc[ci] >= counts[ci]:
                        self.remove(w)
            else:
                # We can just eliminate all words containing c.
                for w in list(self.lookup[ci]):
                    self.remove(w)

    def _apply_exact_matches(self, result: str):
        # The only viable words will be ones that have this char at this position.
        # We only need 'result' here because 'result' contains all exact matches.
        for i, c in enumerate(result):
            if c not in ['.', '?']:
                viable = set()
                for w in self.lookup[c]:
                    if w[i] == c:
                        viable.add(w)
                self.remove_all_except(viable)

    def _apply_inexact_matches(self, guess: str, result: str):
        # Yellow gives us two pieces. It's in the word... but it's not in this position.
        # Build a set of viable words that matches both of those constraints.
        if '?' not in result:
            return
        q_counts = {}
        for i, c in enumerate(guess):
            if result[i] == '?':
                viable = set()
                if c not in q_counts:
                    q_counts[c] = 1
                else:
                    q_counts[c] += 1
                for w in self.lookup[c]:
                    if w[i] != c:
                        viable.add(w)
                self.remove_all_except(viable)
        # Two or more yellows of the same letter can narrow results further.
        # Handle two yellows of the same character, e.g. guess = 'chess' and target = 'assay'
        for c, count in q_counts.items():
            if count >= 2:
                for w in list(self.pool):
                    wc = Counter(w)
                    if wc[c] < q_counts[c]:
                        self.remove(w)
