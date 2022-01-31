# Wordly

Assistant for Wordle. Helps you think of what to guess next.

Send it your guesses and results, it will send back some words you can try.

## Usage 

Run:
`docker run .`

Suppose you're playing a Wordle and the answer is `WORKS`.

So far you've guessed: `SWORD`, `WORDS`, and `WORMS`. `SWORD` had 4 yellows, `WORDS` and `WORMS` each had 4 greens.

Let's post the guesses and see what we get back. 

Request:
```
curl -X POST \
localhost:54345/words \
-H "Content-type: application/json" \
-d '{"SWORD:????.","WORDS":"WOR.S","WORMS":"WOR.S"}'
```

Response:
```
WORKS
WORTS
```

### Request Formatting

The content is a JSON dict of `Guess: Result` string pairs. 

The Guess is the word you guessed.

Result format:
 * '.' for a black letter
 * '?' for a yellow letter
 * The actual letter for a green letter, e.g. 'A' or 'B'.
