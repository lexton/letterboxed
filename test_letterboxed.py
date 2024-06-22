import tempfile
import pytest


from letterboxed import LetterboxedSolver


@pytest.fixture
def wordlist_file():
    words = [
        "apple",
        "ant",
        "banana",
        "cherry",
        "date",
        "elderberry",
        "fig",
        "grape",
    ]
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf8") as f:
        for word in words:
            f.write(f"{word}\n")
        yield f.name


@pytest.fixture
def solver(wordlist_file):
    return LetterboxedSolver(["bde", "a", "n", "t"], wordlist_file=wordlist_file)


@pytest.mark.parametrize(
    "word, expected",
    [
        ("banana", True),  # Valid word
        ("date", True),  # Valid word
        ("ant", False),  # Too short
        ("aant", False),  # Contains forbidden substring 'aa'
        ("abcdg", False),  # Contains forbidden substring 'dd'
        ("Abcdeg", False),  # Proper noun (capital letter)
        ("apple", False),  # Contains doubles
        ("aabcfgha", False),  # Contains forbidden substring 'aa'
    ],
)
def test_is_valid_word(solver, word, expected):
    assert solver.is_valid_word(word) == expected
