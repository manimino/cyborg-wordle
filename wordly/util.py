
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

ALL_POSSIBLE_RESULTS = gen_results()  # list of length 243 containing all possible guess results
