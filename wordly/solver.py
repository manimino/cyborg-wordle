import copy
import random

from typing import *

from wordly.guess import Guess, guess_result
from wordly.word_pool import WordPool
from wordly.word_list import all_wordle_words, top_first_guesses, common_wordle_words_4k


class Solver:
    def __init__(self, hard_mode=False, all_words=True, cost_exp=1.75, max_pool_size=5000, gt_ratio=1):
        self.hard_mode = hard_mode
        # targets represents the remaining possible solutions to a puzzle after applying guesses
        self.targets = WordPool()
        if not all_words:
            self.targets.remove_all_except(common_wordle_words_4k)

        # "valids" contains the words that can be guessed. In Easy Mode, "valids" is the
        # whole Wordle dictionary; in Hard Mode it is a subset of that.
        self.valids = WordPool()
        self.freqs = {}
        for word, freq in all_wordle_words:
            self.freqs[word] = freq

        # params that control the heuristics
        # these have been tuned to produce the best results
        # while still solving the puzzle quickly
        self.cost_exp = cost_exp
        self.max_pool_size = max_pool_size
        self.gt_ratio = gt_ratio

    def get_next_words(self, guesses: List[Guess]) -> List[Tuple[str, int]]:
        """
        Return a list of good words to guess next, sorted so the best one is first.

        First guesses are pre-baked; otherwise that's a really long search
        that's the same every game.
        """
        if len(guesses) == 0:
            random.shuffle(top_first_guesses)
            return [(x, 1) for x in top_first_guesses]

        # apply guess feedback to eliminate invalid targets and guesses.
        for g in guesses:
            self.targets.apply_guess(g)
            if self.hard_mode:
                self.targets.apply_hardmode_constraints(g)
                self.valids.apply_hardmode_constraints(g)
        """
        Return a list of good words to guess next, sorted so the best one is first.

        First guesses are pre-baked; otherwise that's a really long search
        that's the same every game.
        """
        if len(guesses) == 0:
            random.shuffle(top_first_guesses)
            return [(x, 1) for x in top_first_guesses]

        # apply guess feedback to eliminate invalid targets and guesses.
        for g in guesses:
            self.targets.apply_guess(g)
            if self.hard_mode:
                self.targets.apply_hardmode_constraints(g)
                self.valids.apply_hardmode_constraints(g)

        # Handle edge case: if there are only two targets left, you don't want to pick
        # "any guess that reduces the target pool to 1", you want to pick
        # one of the two possible solutions, thereby profiting from the 50/50 chance
        # of guessing correctly.
        if len(self.targets.pool) <= 2:
            return [(random.choice(list(self.targets.pool)), 1)]

        # For non-first guesses, we'll do a search.
        # Ideally, we will try each combination of (valid word, target) and
        # find the one that most likely constrains the target pool to very few words.
        # If the guess and target pools are large, we do some heuristic
        # stuff to reduce or subsample the space before running the all-pairs search.
        targets_subset = copy.deepcopy(self.targets)
        if len(guesses) == 5:
            # only consider possible answers for the final guess
            valids_subset = copy.deepcopy(self.targets)
        else:
            valids_subset = copy.deepcopy(self.valids)
        pool_size = len(self.valids.pool) * len(self.targets.pool)

        # Each pair takes around 0.2ms to check, so we want to reduce pool_size to <= 5000.
        # Start by applying nonmatches from the guess results to the guesses pool. That will
        # encourage guessing of new letters.
        if pool_size > self.max_pool_size:
            # reduce valid guesses pool by removing words with nonmatching letters
            ls = list((g.word, g.result) for g in guesses)
            random.shuffle(ls)
            for guess, result in ls:
                if len(valids_subset.pool) * len(targets_subset.pool) <= self.max_pool_size:
                    # good enough
                    break
                before = copy.deepcopy(valids_subset)
                valids_subset.apply_nonmatches(guess, result)
                if len(valids_subset.pool) < 50:
                    # Over-constraining the guess pool leads to dumb guesses
                    # don't go too hard on this
                    valids_subset = before


        # Subsample the guess and target pools as needed to shrink from there.
        while pool_size > self.max_pool_size:
            if len(valids_subset.pool) >= len(targets_subset.pool) * self.gt_ratio:
                # reduce the guesses pool
                size = max(len(valids_subset.pool) // 2, 10)
                size = min(size, len(valids_subset.pool))
                vpool = random.sample(list(valids_subset.pool), size)
                valids_subset.remove_all_except(vpool)
            else:
                # reduce the targets pool
                size = max(len(targets_subset.pool) // 2, 10)
                size = min(size, len(targets_subset.pool))
                tpool = random.sample(list(targets_subset.pool), size)
                targets_subset.remove_all_except(tpool)
            pool_size = len(targets_subset.pool) * len(valids_subset.pool)

        # now search all (valid guess, target) pairs to find the best guess from the
        # reduced pools.
        guess_scores = []
        best_score = float('inf')
        guess_pool = list(valids_subset.pool)
        targets_pool = list(targets_subset.pool)

        for guess in guess_pool:
            guess_score = 0

            # now, let's see what the solution space looks like after applying this guess
            new_guesses = copy.deepcopy(guesses)
            for i, tw in enumerate(targets_pool):
                targets_copy = copy.deepcopy(targets_subset)
                result = guess_result(guess, tw)
                new_guesses.append(Guess(guess, result))
                for g in new_guesses:
                    targets_copy.apply_guess(g)
                    n_left = len(targets_copy.pool)
                    guess_score += n_left**self.cost_exp
                if guess_score > best_score:
                    # we already know this guess is worse than one we have
                    # bail outta this trial
                    break
            if guess_score < best_score:
                best_score = guess_score
                guess_scores.append((guess, round(guess_score, 3)))

        print('guess pool size:', len(guess_pool), 'target pool size:', len(targets_pool))
        print('valids:', len(self.valids.pool), 'ntargets:', len(self.targets.pool))
        guess_scores.sort(key=lambda x: x[1])
        return guess_scores
