import random

from collections import Counter
from wordlist import dictionary

HMM = '?'
NO = '_'


class Game():
    def __init__(self):
        self.target = random.choice(dictionary)

    def guess(self, word):
        counts = Counter(self.target)
        ret = []
        for i in range(len(word)):
            c = word[i]
            # match
            if self.target[i] == c:
                ret.append(c)
                if c in counts:
                    counts[c] -= 1
                continue
            # right letter, wrong spot
            if c in counts and counts[c] > 0:
                ret.append(HMM)
                if c in counts:
                    counts[c] -= 1
                continue
            # nope
            if c not in counts or counts[c] <= 0:
                ret.append(NO)
        return ''.join(ret)


def solver(results):
    """
    :param results: dict of {guessed word: output string}
    :return: next guess to make
    """
    # totally random guess, replace with real solver
    return random.choice(dictionary)


def solve():
    g = Game()
    guesses = dict()
    n = 0
    while True:
        w = solver(guesses)
        result = g.guess(w)
        n += 1
        guesses[w] = result
        print(w)
        print(result)
        if w == g.target:
            print('you win!')
            print('and it only took', n, 'guesses')
            return


def play():
    g = Game()
    while True:
        w = input('> ')
        if w == g.target:
            print('you win!')
            return
        else:
            print(' ', g.guess(w))


# play()
solve()
