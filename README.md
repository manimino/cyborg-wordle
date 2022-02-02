# Wordly

Command-line Wordle game with optional AI assistance.

Supports normal mode and hard mode.

The AI is fast and has a win rate over 99%. 

Type '?' to get a hint from the AI if you're stuck.

## Usage 

To play: `python wordly.py`

Hard mode: `python wordly.py -h` or `--hard`

AI-only game: `python wordly.py -a` or `--ai`. Can be used with hard mode.

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
Learning from the Wordly AI is a great way to train your Wordle skills.

When a hint is requested, the AI does not exhaustively search every possible guess and solution.
That would take days of compute time, even in a compiled language. 

Instead, this AI uses various heuristics and probablistic methods to produce an excellent guess.
It has been shown that heuristics closely approximate optimal play. Using these, Wordly produces a 
high-quality hint in under 1 second. 
