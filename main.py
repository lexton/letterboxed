#!/usr/bin/env python3

import sys
from typing import List, Set

import click

from nyt import nyt_lb_game_data_today
from letterboxed import LetterboxedSolver


@click.command(help="A generic letterbox solver")
@click.argument("words", nargs=-1)
@click.option(
    "--wordlist",
    type=click.Choice(
        ["google-10k", "test", "unix", "scrabble", "wordle"], case_sensitive=False
    ),
    default="scrabble",
    help="Wordlist that should be used to generate solutions",
)
@click.option("--max-results", default=-1, help="Limit the number of rendered results")
@click.option("--max-word-chain", default=3, help="Limit the length of the word chains")
@click.option("--debug", is_flag=True, help="Enable debug logging")
def main(words: List[str], wordlist, max_results, max_word_chain, debug):
    results: Set[str] = set()
    result_count = 0
    chain_depth = 1

    if len(words) == 0:
        print("Fetching Letter-Boxed from NYT")
        metadata = nyt_lb_game_data_today()
        words = "-".join(metadata["sides"]).lower().split("-")
        solution = "-".join(metadata["ourSolution"]).lower()

        print(f"Loaded ID: {metadata['id']} | Date: {metadata['date']}")
        print(f"Edges: {metadata['sides']} | Official Solution: {solution}")
        if debug:
            print(f"Metadata: {metadata}")

    solver = LetterboxedSolver(
        words,
        wordlist_file=f"words/{wordlist}.txt",
    )

    if debug:
        print(
            f"Result Filters: max_word_chain: {max_word_chain} max_results: {max_results}"
        )
        print(f"Allowed Chars: {solver.allowed_chars}")
        print(f"Forbidden Substrings: {solver.forbidden_substrings}")

    print(
        f"Wordlist: {wordlist} | Candidate Words: {sum(len(v) for v in solver.prefix.values())}"
    )

    for result in solver:
        # filter the result collection

        if len(result) > max_word_chain:
            break

        if max_results != -1 and result_count > max_results:
            break

        # print results that are equal in quality all at once
        if chain_depth != len(result):
            if len(results) != 0:
                print(f"{chain_depth} words combinations: {len(results)} results")
                for w in sorted(results):
                    print(f"  {w}")

            # reset active results
            chain_depth, results = len(result), set()

        result_count += 1
        results.add("-".join(result))

    if result_count == 0:
        print("No valid letter boxed solutions found")
        sys.exit(1)

    print(f"{chain_depth} words combinations: {len(results)} results")
    for w in sorted(results):
        print(f"  {w}")


if __name__ == "__main__":
    main()
