# Cyborg Wordle

Command-line Wordle game with optional assistance from your AI pal, Wordly.

Supports normal mode and hard mode.

Wordly wins on over 99% of all Wordle puzzles.

Type '?' to get a hint from the AI if you're stuck.

![demo](images/demo_daddy.gif)

## Usage 

To play: `python main.py`.

Hard mode: `python main.py --hard` 

Watch the AI play: `python main.py --ai`. Can be used with hard mode.

## Design Details

### Game

Just as in Wordle, you have six guesses to find a target five-letter word.

In hard mode, information from previous guesses must be used.

Solutions will always be in the top 4000 most common English words. However, any 5-letter word
may be used as a guess.

### AI Details

Wordle is a solved game in both easy and hard modes. There exists a tree of guesses
that will always win the game. However, following the same decision tree every game isn't much fun.

Thus, this implementation is a 'cyborg' game, where a human plays with optional computer assistance. 
Learning from Wordly is a great way to train your Wordle skills.

When a hint is requested, Wordly does not exhaustively search every possible guess and solution.
That would take days of compute time, even in a compiled language. 

Instead, Wordly uses various heuristics and probablistic methods to produce an excellent guess.
It has been shown that heuristics closely approximate optimal play. Using these, Wordly produces a 
high-quality hint in under 1 second. 
