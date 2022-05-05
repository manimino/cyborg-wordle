
class ColoredText:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colorize(guess: str, result: str) -> str:
    """
    Applies color scheme to guess given result.
    """
    ret = []
    for i in range(len(guess)):
        if result[i] == '?':
            ret.append(ColoredText.WARNING + guess[i] + ColoredText.ENDC)
        elif result[i] == '.':
            ret.append(ColoredText.FAIL + guess[i] + ColoredText.ENDC)
        else:
            ret.append(ColoredText.OKGREEN + guess[i] + ColoredText.ENDC)
    return ''.join(ret)

