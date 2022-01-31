import random

from wordly.game import make_guess
from wordly.solver import Solver
from wordly.word_list import all_wordle_words

def play_interactive():
    """
    Plays the game interactively from the command line
    """
    valid = set(x[0] for x in all_wordle_words)
    target, _ = random.choice(all_wordle_words)

    while True:
        w = input('> ')
        w = w.upper()
        if w == "?":  # hax
            print(target)
            continue

        if len(w) != 5 or w not in valid:
            print('Invalid word:', w)
            continue

        if w == target:
            print('you win!')
            return
        else:
            print(' ', make_guess(w, target))

def solve():
    target, _ = random.choice(all_wordle_words)
    s = Solver()
    guesses = {}
    guess = 'FROND'
    while True:
        result = make_guess(guess, target)
        guesses[guess] = result
        print(guess)
        print(result)
        if guess == target:
            print('got it in', len(guesses), 'guesses')
            return
        # update pools based on guesses
        s.valids.apply_nonmatches(guess, result)
        s.targets.apply_guesses(guesses)
        if len(s.targets.pool) == 1:
            guess = s.targets.pool.pop()
        else:
            next_words = s.get_next_words(guesses)
            print(next_words[:min(10, len(next_words))])
            guess = next_words[0][0]


# play_interactive()
solve()
