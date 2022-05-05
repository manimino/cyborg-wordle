import random

from wordly.color import ColoredText
from wordly.guess import Guess, guess_result
from wordly.word_list import common_wordle_words_4k, all_wordle_words
from wordly.word_pool import WordPool


ERR_NON_5_LETTER = 'Need a 5-letter word.'
ERR_HARD_MODE = '{} violates the hard mode rules.\nYou must reuse all correct letters and positions.'
ERR_NON_WORD = '{} is not a word.'


class Game:
    def __init__(self, hard_mode=False, all_words=False):
        if all_words:
            # an AI is playing, let's give them a challenge by allowing any 5-letter word
            self.target = random.choice(all_wordle_words)[0]
        else:
            # a squishy human wants to feel smart, let's give them an easier challenge
            self.target = random.choice(common_wordle_words_4k)
        self.hard_mode = hard_mode
        self.guesses = []
        self.valid_word_set = WordPool()
        self.valid_guesses = WordPool()  # used in hard mode only

    def guess_word(self, word: str) -> str:
        """Guess a word. Return empty string on success, error string if unsuccessful."""
        word = word.upper()
        if len(word) != 5:
            return ERR_NON_5_LETTER
        if word not in self.valid_word_set.pool:
            return ERR_NON_WORD.format(word)
        if self.hard_mode and word not in self.valid_guesses.pool:
            return ERR_HARD_MODE.format(word)
        result = guess_result(word, self.target)
        guess = Guess(word, result)
        self.guesses.append(guess)
        if self.hard_mode:
            self.valid_guesses.apply_hardmode_constraints(guess)
        return ''

    def render_cli(self):
        """Print game state to terminal"""
        print("")
        for g in self.guesses:
            s = []
            for i, c in enumerate(g.word):
                if g.result[i] == '?':
                    # inexact match
                    s.append(ColoredText.WARNING + c + ColoredText.ENDC)
                elif g.result[i] == '.':
                    # nonmatch
                    s.append(ColoredText.FAIL + c + ColoredText.ENDC)
                else:
                    # match
                    s.append(ColoredText.OKGREEN + c + ColoredText.ENDC)
            print(' ' * 12 + ' '.join(s))
        n_blank = 6 - len(self.guesses)
        for _ in range(n_blank):
            print(' ' * 12 + ' '.join(['_'] * 5))
        print('')

