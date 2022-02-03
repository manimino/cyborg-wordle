import random
from collections import Counter

from wordly.game import make_guess
from wordly.solver import Solver
from wordly.util import ColoredText
from wordly.word_list import all_wordle_words, common_wordle_words_4k


def render_game(guesses: list):
    print("")

    for guess, result in guesses:
        s = []
        for i, c in enumerate(guess):
            if result[i] == '?':
                # inexact match
                s.append(ColoredText.WARNING + c + ColoredText.ENDC)
            elif result[i] == '.':
                # nonmatch
                s.append(ColoredText.FAIL + c + ColoredText.ENDC)
            else:
                # match
                s.append(ColoredText.OKGREEN + c + ColoredText.ENDC)
        print(' '*12 + ' '.join(s))
    n_blank = 6 - len(guesses)
    for _ in range(n_blank):
        print(' '*12 + ' '.join(['_']*5))
    print('')


def keyboard_str(guesses: list) -> str:
    letters = 'abcdefghijklmnopqrstuvwxyz'.upper()
    letter_colors = dict(zip(letters, ['']*26))
    for guess, result in guesses:
        for i, c in enumerate(guess):
            if result[i] == '?':
                # inexact match
                letter_colors[c] = ColoredText.WARNING
            elif result[i] == '.':
                # nonmatch
                letter_colors[c] = ColoredText.FAIL
            else:
                # match
                letter_colors[c] = ColoredText.OKGREEN
    ret = []
    for l in letters:
        ret.append(letter_colors[l] + l + ColoredText.ENDC)
    return ' '*3 + '(' + ''.join(ret) + ')'


def play_interactive():
    """
    Plays the game interactively from the command line
    Targets will be in the 4000 most common English words that are in the
    Wordle dictionary, because solutions like ESNES and ROLAG are rage-inducing.
    """
    print("\n-----=====  It's Wordly Time!  =====-----")
    print("Guess a five-letter word, or ? for a hint.")
    valid = set(x[0] for x in all_wordle_words)
    target = random.choice(common_wordle_words_4k)
    guesses = []
    while True:
        render_game(guesses)
        w = input(keyboard_str(guesses) + ' > ')
        w = w.upper()

        if w == "?":  # hax
            s = Solver()
            ai_words = s.get_next_words(dict(guesses))
            print(ai_words)
            ai_word = ai_words[0][0]
            print('   Try the word "{}".'.format(ai_word))
            continue

        if len(w) != 5 or w not in valid:
            print('Invalid word:', w)
            continue

        result = make_guess(w, target)
        guesses.append((w, result))

        if w == target:
            render_game(guesses)
            print('you win!')
            return


def solve(s: Solver):
    target, _ = random.choice(all_wordle_words)
    guesses = {}
    guess = random.choice(common_wordle_words_4k)
    while True:
        result = make_guess(guess, target)
        guesses[guess] = result
        print(guess)
        print(result)
        if guess == target:
            print('got it in', len(guesses), 'guesses')
            return len(guesses)
        # update pools based on guesses
        s.targets.apply_guesses(guesses)
        if len(s.targets.pool) == 1:
            guess = s.targets.pool.pop()
        else:
            next_words = s.get_next_words(guesses)
            print(next_words[:min(10, len(next_words))])
            guess = next_words[0][0]


def fit_params():
    all_results = []
    N_TRIALS = 1000
    cost_exps = [1.75]
    mpoolsizes = [5000]
    gt_ratios = [1.0]
    modes = [True, False]
    import math
    tot = math.prod([len(x) for x in [cost_exps, mpoolsizes, gt_ratios, modes]])
    tot *= N_TRIALS
    print('running', tot, 'trials')
    tnum = 0
    for hard_mode in modes:
        for cost_exp in cost_exps:
            for max_pool_size in mpoolsizes:
                for gt_ratio in gt_ratios:

                    results = []
                    for i in range(N_TRIALS):
                        tnum += 1
                        if tnum % 10 == 2:
                            print(round(tnum / tot * 100, 3), '% done')
                        s = Solver(hard_mode=hard_mode,
                                   max_pool_size=max_pool_size,
                                   gt_ratio=gt_ratio,
                                   cost_exp=cost_exp)
                        result = solve(s)
                        results.append(result)
                    counts = Counter(results)
                    losses = 0
                    mean = round(sum(results) / len(results), 3)
                    for k in counts.keys():
                        if k > 6:
                            losses += 1
                    losses = round(losses / len(results) * 100, 3)
                    all_results.append((hard_mode, cost_exp, max_pool_size, gt_ratio, mean, losses))
    print('hard_mode, cost_exp, max_pool_size, gt_ratio, mean, losses')
    for r in all_results:
        print(str(r) + ',')
    print(tot)


if __name__ == '__main__':
    play_interactive()
    # fit_params()
    #s = Solver(hard_mode=False)
    #solve(s)