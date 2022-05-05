from wordly.guess import Guess
from wordly.solver import Solver


def test_solver():
    s = Solver()
    s.get_next_words([Guess('KNIFE', '.....')])
