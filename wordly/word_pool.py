from collections import Counter

from wordly.word_list import all_wordle_words


"""
A WordPool represents a set of words, with convenience functions for fast lookup and removal.

Initially a word pool contains the whole Wordle dictionary; applying constraints (guesses and results)
will remove words from the pool.

Used by the Solver to represent the set of possible solutions and the set of valid guesses.
"""

class WordPool():

    def __init__(self):
        self.pool = set()  # all available words, initially the entire Wordle dictionary.
        self.lookup = {}  # lookup table of character: word to speed up queries

        for word, _ in all_wordle_words:
            self.pool.add(word)

        for w in self.pool:
            for c in w:
                if c not in self.lookup:
                    self.lookup[c] = set()
                self.lookup[c].add(w)

    def remove(self, w: str):
        # removes a word from the data structure
        for c in w:
            if w in self.lookup[c]:
                self.lookup[c].remove(w)
        if w in self.pool:
            self.pool.remove(w)

    def remove_all_except(self, these: set):
        # removes all words except for 'these'
        for w in self.pool.difference(these):
            self.remove(w)

    def match_char_pos(self, char: str, pos: int) -> set:
        # get all words matching a char in a specific position
        matches = set()
        for w in self.lookup[char]:
            if w[pos] == char:
                matches.add(w)
        return matches

    def __repr__(self):
        if len(self.pool) <= 10:
            return 'Words remaining: {} {}'.format(len(self.pool), list(self.pool))
        else:
            return 'Words remaining: {} {} ...'.format(len(self.pool), list(self.pool)[:10])

    # -- Guess related functions -- #
    def apply_guesses(self, guesses: dict):
        # applies guesses to the pool, removing nonmatching words
        # used when the WordPool represents the set of possible solutions
        for guess, result in guesses.items():
            self._apply_exact_matches(result)
            self.apply_nonmatches(guess, result)
            self._apply_inexact_matches(guess, result)

    def apply_hardmode_constraints(self, guesses: dict):
        """
        Apply guesses / results to the pool, removing words that can't be used in hard mode.
        In hard mode, a word is only usable if it keeps exact and inexact matches from any previous guess.
        Inexact matches are allowed to be in any spot, even the same spot they were in a previous guess;
        only their presence matters. That's a bit different than the _apply_inexact_matches logic.
        """
        # apply greens
        for _, result in guesses.items():
            self._apply_exact_matches(result)
        # apply yellows
        # first, trim down pool to only words that contain at least one of each yellow letter
        for guess, result in guesses.items():
            for i, rc in enumerate(guess):
                c = guess[i]
                if rc == '?':
                    self.remove_all_except(self.lookup[c])
        # now, handle case where there are 2+ yellows of the same letter
        q_counts = Counter(guess[i] for i in range(len(result)) if result[i] == '?')
        for w in set(self.pool):
            w_counts = Counter(w)
            for c, count in q_counts.items():
                if w_counts[c] < q_counts[c]:
                    self.remove(w)

    def apply_nonmatches(self, guess: str, result: str):
        # We now know some letters that are definitely not in the word.
        # Eliminate those from the dictionary.
        counts = Counter(guess)
        for i, c in enumerate(guess):
            if result[i] == '.':
                # is there a yellow or green c elsewhere in the guess? we need to check that
                if counts[c] == 1:
                    # no other instances of c. We can just eliminate all words containing c.
                    for w in list(self.lookup[c]):
                        self.remove(w)
                else:
                    # eliminate all words with c at this position.
                    for w in self.match_char_pos(c, i):
                        self.remove(w)
                    # Also eliminate all words with a c-count greater or equal to the c-count in the guess.
                    # if there were another c in the target word, this position would've been yellow.
                    for w in list(self.pool):
                        wc = Counter(w)
                        if wc[c] >= counts[c]:
                            self.remove(w)


    def _apply_exact_matches(self, result: str):
        # The only viable words will be ones that have this char at this position.
        # We only need 'result' here because 'result' contains all exact matches.
        for i, c in enumerate(result):
            if c != '.' and c != '?':
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