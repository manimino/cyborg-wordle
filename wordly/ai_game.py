import random

from wordly.color import colorize
from wordly.game import Game
from wordly.solver import Solver
from wordly.word_list import all_wordle_words


def play_ai_game(hard_mode):
    game = Game(hard_mode=hard_mode, all_words=True)
    s = Solver(hard_mode=hard_mode)
    target, _ = random.choice(all_wordle_words)
    word = s.get_next_words(game.guesses)[0][0]
    while True:
        result = game.guess_word(word)
        if result:
            raise ValueError(result)
        print('guessed:', word)
        g = game.guesses[-1]
        print('results:', colorize(g.word, g.result))
        print('')
        if word == game.target:
            print('got it in', len(game.guesses), 'guesses')
            return len(game.guesses)
        # update pools based on guesses
        s.targets.apply_guess(game.guesses[-1])
        # determine next word
        next_words = s.get_next_words(game.guesses)
        print('thinking:', next_words[:min(10, len(next_words))])
        if len(s.targets.pool) < 10:
            print('possibilities left:', list(s.targets.pool))
        else:
            print('possibilities left:', len(s.targets.pool))
        word = next_words[0][0]
