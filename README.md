# Solver for the NYT Letter Boxed game

Simple project to warm back up again into coding.

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
1. Load todays question (from the CLI or ask NYT website)
1. Pick and load a wordlist
1. Filter the wordlist
1. BFS (by number of words) to generate results, always making progress towards using all letters
1. Render Results

