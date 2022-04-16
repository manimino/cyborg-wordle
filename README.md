# Cyborg Wordle

Command-line Wordle game with optional assistance from your AI pal, Wordly.

Supports normal mode and hard mode.

Type '?' to get a hint from Wordly if you're stuck.

![demo](images/demo_daddy.gif)

## Usage 

To play: `python main.py`.

Hard mode: `python main.py --hard` 

Watch Wordly play: `python main.py --ai`. AI mode uses a harder word list.

Wordly is a clever Wordle AI. It wins over 99% of all Wordles.

## Design Details

### Game

Just as in Wordle, you have six guesses to find a target five-letter word.

In hard mode, information from previous guesses must be used.

Solutions will always be in the top 4000 most common English words. However, any 5-letter word
may be used as a guess.

### AI Details

Wordle is a solved game in both easy and hard modes. There exists a tree of guesses
that will always win the game. But following the same decision tree every game isn't much fun.
And writing an AI that can play from any game state is more interesting too.

Thus, this implementation is a 'cyborg' game, where a human plays with optional computer assistance. 
Learning from Wordly is a great way to train your Wordle skills.

When a hint is requested, Wordly does not exhaustively search every possible guess and solution.
Instead, Wordly considers a few hundred words and picks one that will narrow down the pool of possible answers.
 
### Further reading

Wordly's heuristics are based on these sources.

https://www.poirrier.ca/notes/wordle
http://sonorouschocolate.com/notes/index.php?title=The_best_strategies_for_Wordle
