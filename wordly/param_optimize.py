from collections import Counter

from wordly.ai_game import play_ai_game
from wordly.solver import Solver


def fit_params():
    # This was used to run experiments to find good defaults for each solver param
    all_results = []
    N_TRIALS = 1000
    cost_exps = [1.75]
    mpoolsizes = [5000]
    gt_ratios = [1.0]
    modes = [True, False]
    import math
    tot = math.prod([len(x) for x in [cost_exps, mpoolsizes, gt_ratios, modes]])
    tot *= N_TRIALS
    print('running', tot, 'trials')
    tnum = 0
    for hard_mode in modes:
        for cost_exp in cost_exps:
            for max_pool_size in mpoolsizes:
                for gt_ratio in gt_ratios:

                    results = []
                    for i in range(N_TRIALS):
                        tnum += 1
                        if tnum % 10 == 2:
                            print(round(tnum / tot * 100, 3), '% done')
                        s = Solver(hard_mode=hard_mode,
                                   max_pool_size=max_pool_size,
                                   gt_ratio=gt_ratio,
                                   cost_exp=cost_exp)
                        result = play_ai_game(s)
                        results.append(result)
                    counts = Counter(results)
                    losses = 0
                    mean = round(sum(results) / len(results), 3)
                    for k in counts.keys():
                        if k > 6:
                            losses += 1
                    losses = round(losses / len(results) * 100, 3)
                    all_results.append((hard_mode, cost_exp, max_pool_size, gt_ratio, mean, losses))
    print('hard_mode, cost_exp, max_pool_size, gt_ratio, mean, losses')
    for r in all_results:
        print(str(r) + ',')
    print(tot)

