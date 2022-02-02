
def gen_results():
    n = 0
    ls = ['']
    while n < 5:
        new_ls = []
        for item in ls:
            new_ls.append(item + '.')
            new_ls.append(item + '?')
            new_ls.append(item + '*')  # means 'match'. Replaced by letter when used.
        ls = new_ls
        n += 1
    return ls

# list of length 243 containing all possible guess results
ALL_POSSIBLE_RESULTS = gen_results()


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
