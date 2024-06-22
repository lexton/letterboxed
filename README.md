# CLI Solver for the NYT Letter Boxed game

## Intro:

Game: http://nytimes.com/puzzles/letter-boxed

Goal: find the shortest number of words that will allow you to use every node on the edge

Rules:
1. The same edge can't be used consecutively
1. The next word must start with the ending letter of the last word
1. All letters must be used at least once
1. No additional letters may be used
1. Words must be at least 3 letters long


## General Approach
1. Load todays question (directly from passed args or ask NYT website)
1. Pick and load a wordlist
1. Filter the wordlist removing any invalid or illegal words
1. BFS (by number of words) to generate results, always making progress towards using all required letters
1. Render Results

## Solution Details

### Generic Solution
This solver should solve flexibly sized letterboxes

1. Edges don't need to be a uniform length
1. Can be any number of edges, so doesn't need to be a square, could be a triangle, octagon or even a line (but it won't find any solutions)

## Interesting Considerations
* Total length of word is unimportant, the length of the unique letter set for each word is important
* Store each word alongside the remaining characters for the overall solution makes this easy to look up
* Index each word based on the first character (since we will heavily use this for finding next words)


## Usage

`docker run lukeex/letterboxed:latest`

or if you want to run it locally from source



``` bash
$ python3 -m venv venv
$ pip3 install -r requirements.txt
$ ./main.py # --help will give you the CLI options including word list and max number of words to generate etc
```