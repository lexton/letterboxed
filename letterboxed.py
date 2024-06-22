from collections import defaultdict, deque
from typing import List, Dict
from itertools import product


class LetterboxedSolver:
    """LetterboxSolver

    This will generate solutions to the NYT letterboxed game.

    """

    def __init__(self, edges: List[str], wordlist_file=None, min_length=3):

        # initialize validators first
        self.forbidden_substrings: set[str] = set()
        self.min_length = min_length

        # process edges
        self.allowed_chars: set[str] = set("".join(edges))
        for w in edges:
            # note: itertools.permutations doesn't include repeating values
            for p in product(w, repeat=2):
                self.forbidden_substrings.add("".join(p))

        # load dictionary data

        # prefix is an index of the first character in each word
        self.prefix: Dict[str, set] = defaultdict(set)

        # count is the unique character count for each words, its used for ordering first pick
        self.count: Dict[int, set] = defaultdict(set)

        if wordlist_file:
            self.load_wordlist(wordlist_file)

    def is_valid_word(self, word: str) -> bool:

        # ignore proper noun
        # nit: maybe this is redundant since we sanitize input to be all lower case
        if word[0].isupper():
            return False

        # ensure min length is satisfied
        if len(word) <= self.min_length:
            return False

        # Check if the word contains only allowed characters
        if not all(c in self.allowed_chars for c in word):
            return False

        # Check if the word contains any forbidden substrings
        for substring in self.forbidden_substrings:
            if substring in word:
                return False

        return True

    def load_wordlist(self, path) -> None:
        # we assume that the whole wordlist will fit into memory easily
        with open(path, "r", encoding="utf8") as f:
            for l in f.readlines():
                self.insert(l.strip())

    def insert(self, word) -> None:
        if not self.is_valid_word(word):
            return

        # create multiple indexes on insertion
        self.prefix[word[0]].add(word)
        self.count[len(set(word))].add(word)

    def first_word_choice(self):
        # start with the words with the most unique characters and then alphabetically
        for _, v in sorted(self.count.items(), reverse=True):
            for w in sorted(v):
                yield w

    def next_word(self, first_char: str, left: set):
        # cache the results we aren't going to immediately use
        candidates = set()
        for w in self.prefix[first_char]:
            r = len(left - set(w))

            # NOTE: there may be situations where a joining word would make no progress
            # but would allow the next stage to be reached by pivoting on a different char prefix
            # catching this case would add substantial complexity

            # no progress, skip
            if r == len(left):
                continue

            # immediate solution, give that first
            if r == 0:
                yield w
                continue

            candidates.add(w)

        for s in candidates:
            yield s

    def __iter__(self):
        """convenience function to allow us to treat the class as a generator"""
        return self.gen_solutions()

    def gen_solutions(self):
        # BFS implementation
        queue = deque([])
        for w in self.first_word_choice():
            left = self.allowed_chars - set(w)

            # NOTE: its rare, but we may find a single word that solves the game
            if len(left) == 0:
                yield w
                continue

            queue.append(([w], left))

        while queue:
            words, left = queue.popleft()
            for n in self.next_word(words[-1][-1], left):
                char_diff = left - set(n)
                word_chain = words + [n]

                # we have found a finished chain
                if len(char_diff) == 0:
                    yield word_chain

                # we need to go to next depth, but wrap up this depth first
                else:
                    queue.append((word_chain, char_diff))
