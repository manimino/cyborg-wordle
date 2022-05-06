class ColoredText:
    NONE = '\033[0m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;93m'
    BLUE = '\033[1;34m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colorize(guess: str, result: str) -> str:
    """
    Applies color scheme to guess given result.
    """
    ret = []
    for i in range(len(guess)):
        if result[i] == '?':
            ret.append(ColoredText.YELLOW + guess[i] + ColoredText.NONE)
        elif result[i] == '.':
            ret.append(ColoredText.RED + guess[i] + ColoredText.NONE)
        else:
            ret.append(ColoredText.GREEN + guess[i] + ColoredText.NONE)
    return ''.join(ret)

