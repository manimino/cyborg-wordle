import argparse
from collections import Counter

from wordly.cli_game import CommandLineGame
from wordly.ai_game import play_ai_game


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ai', action='store_true')
    parser.add_argument('--hard', action='store_true')
    parser.add_argument('--stats', action='store_true')
    args = parser.parse_args()

    if args.ai:
        if args.stats:
            results = []
            for i in range(100):
                results.append(play_ai_game(args.hard, all_words=False))
                c = Counter(results)
                for n in range(2, max(c.keys())+1):
                    print(f'{n} guesses:', c.get(n, 0))
        else:
            play_ai_game(args.hard)
    else:
        CommandLineGame(hard_mode=args.hard).cmdloop()


if __name__ == '__main__':
    main()
