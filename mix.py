from termcolor import colored
from wordly.color import ColoredText


s = ''
for i in range(3):
    s += colored('X', 'red') + colored('Y', None)
print(repr(s))

s = ColoredText.FAIL + 'X' + ColoredText.ENDC + 'Y'
print(repr(s))

