import cmd

from wordly.color import ColoredText
from wordly.game import Game
from wordly.solver import Solver


def keyboard_str(guesses: list) -> str:
    letters = 'abcdefghijklmnopqrstuvwxyz'.upper()
    letter_colors = dict(zip(letters, ['']*26))
    for g in guesses:
        for i, c in enumerate(g.word):
            if g.result[i] == '?':
                # inexact match
                letter_colors[c] = ColoredText.YELLOW
            elif g.result[i] == '.':
                # nonmatch
                letter_colors[c] = ColoredText.RED
            else:
                # match
                letter_colors[c] = ColoredText.GREEN
    ret = []
    for c in letters:
        if letter_colors[c]:
            ret.append(letter_colors[c] + c + ColoredText.NONE)
        else:
            ret.append(c)
    return ' '*3 + '(' + ''.join(ret) + ')'


class CommandLineGame(cmd.Cmd):
    """
    Play the game interactively from the command line.

    Targets will be in the 4000 most common English words that are in the
    Wordle dictionary. The cmd superclass is used for its nice command history.
    """

    def __init__(self, hard_mode=False):
        super().__init__()
        self.game = Game(hard_mode=hard_mode)
        print("\n-----=====  It's Wordly Time!  =====-----")
        print("Guess a five-letter word, or ? for a hint.")
        self.prompt = keyboard_str(self.game.guesses) + ' > '

    def preloop(self) -> None:
        self.game.render_cli()

    def parseline(self, line):
        return None, None, line

    def default(self, line):
        # renders the prompt and gets a response
        w = line.strip().upper()
        if w == 'EXIT':
            return True

        if w == "?":  # get a hint from the AI
            s = Solver(hard_mode=self.game.hard_mode)
            ai_words = s.get_next_words(self.game.guesses)
            ai_word = ai_words[0][0]
            self.game.render_cli()
            print(ColoredText.BLUE + ' '*7 + 'Try the word "{}".\n'.format(ai_word) + ColoredText.NONE)
            return

        result_str = self.game.guess_word(w)
        if result_str:
            print(ColoredText.BLUE + ' ' * 7 + result_str + ColoredText.NONE)

        self.prompt = keyboard_str(self.game.guesses) + ' > '

        self.game.render_cli()
        if w == self.game.target:
            if self.game.hard_mode:
                print(ColoredText.BLUE + ' '*12 + '*You win!*' + ColoredText.NONE)
            else:
                print(ColoredText.BLUE + ' '*12 + 'You win!' + ColoredText.NONE)
            return True
        elif len(self.game.guesses) == 6:
            print(ColoredText.RED + ' '*12 + 'You lost.' + ColoredText.NONE)
            print(ColoredText.RED + ' '*12 + 'The word was: '.format(self.game.target) +
                  ColoredText.NONE + ColoredText.GREEN + self.game.target + ColoredText.NONE)
            return True
