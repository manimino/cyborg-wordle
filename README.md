# Wordly

Command-line Wordle game with a hint engine and a fast heuristic solver.

## Usage 

Clone / install
```
git clone git@github.com:shoreofwonder/wordly
pip install ./wordly
```

Then run `wordly` to play. 

## Design Details

### Game

Supports normal and hard modes. In hard mode, information from guesses must be used.

Solutions will always be in the top 4000 most common English words. However, all 12,972 Wordle words
may be used as guesses.


### Hints