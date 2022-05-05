from dataclasses import dataclass
from collections import Counter


INEXACT_MATCH = '?'
NON_MATCH = '.'


@dataclass
class Guess:
    word: str
    result: str


def guess_result(word: str, target: str) -> str:
    """
    Compare word and target to determine correct / partially correct letters.

    Example:
        Target: "SWIMS"
        Guess:  "GRASS"
        Return: "...?S"
    Return string indicates that the last S matches, the other S is an inexact match, and the
    rest of the letters are incorrect.
    """
    counts = Counter(target)  # tracks matchable letters, removed as they are matched.
    ret = [NON_MATCH] * 5

    # handle exact matches first
    for i in range(len(word)):
        c = word[i]
        if target[i] == c:
            ret[i] = c
            counts[c] -= 1

    # now do inexact matches
    for i in range(len(word)):
        if ret[i] == NON_MATCH:
            c = word[i]
            if c in counts and counts[c] > 0:
                ret[i] = INEXACT_MATCH
                counts[c] -= 1
    return ''.join(ret)
