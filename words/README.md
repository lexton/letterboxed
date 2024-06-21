# Wordlists

This is an interesting flavor for how you can solve the letterbox

Letting you pick which wordlist is allowed.

## Specifics

### Google-10k

* Sourced from: https://github.com/first20hours/google-10000-english
* Caveats: proper nouns not removed - will not generate always valid results, names are present

### Unix
* Sourced from `/usr/share/dict/words`
* Proper nouns are capitalized at least, so are automatically removed since we work entirely in lower case
* Doesn't contain all english words: e.g. humiliated

## Wordle
* Source: https://github.com/tabatkins/wordle-list
* Notes: Manually sorted

## Test
* Sourced from: my brain
* Used for test cases, not an actually useful wordlist

## Scrabble
* Official wordlist
* https://boardgames.stackexchange.com/questions/38366/latest-collins-scrabble-words-list-in-text-file