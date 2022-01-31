from collections import Counter

HMM = '?'
NO = '.'


def make_guess(word: str, target: str):
    counts = Counter(target)
    ret = [NO] * 5
    # handle matches first
    for i in range(len(word)):
        c = word[i]
        if target[i] == c:
            ret[i] = c
            if c in counts:
                counts[c] -= 1
            continue

    # now do inexact matches
    for i in range(len(word)):
        if ret[i] != NO:
            continue
        c = word[i]
        # right letter, wrong spot
        if c in counts and counts[c] > 0:
            ret[i] = HMM
            if c in counts:
                counts[c] -= 1
            continue
    return ''.join(ret)
