"""Wordle Solver Core Engine.

This module provides functions to filter a dictionary of words based on 
a series of Wordle-style guesses and their corresponding color feedback responses.
"""

from typing import List


def read_dictionary() -> List[str]:
    """Reads words from standard input until the sentinel '###' is encountered.

    Returns:
        List[str]: A list of words defining the available dictionary.
    """
    words: List[str] = []
    while True:
        word = input().strip()
        if word == "###":
            break
        words.append(word)
    return words


def compute_response(target: str, guess: str) -> str:
    """Simulates the Wordle feedback logic for a given guess against a target word.

    Uppercase characters represent exact matches (Green).
    Lowercase characters represent misplaced matches (Yellow).
    Periods ('.') represent misses (Gray).

    Args:
        target (str): The hidden correct word.
        guess (str): The word guessed by the player.

    Returns:
        str: The formatted response string showing match states.
    """
    target = target.upper()
    guess = guess.upper()

    result: List[str] = ["."] * len(target)
    target_used: List[bool] = [False] * len(target)

    # First pass: Identify exact matches (Green/Correct position)
    for i in range(len(target)):
        if guess[i] == target[i]:
            result[i] = guess[i]
            target_used[i] = True

    # Second pass: Identify partial matches (Yellow/Wrong position)
    for i in range(len(target)):
        if result[i] == ".":
            for j in range(len(target)):
                if not target_used[j] and guess[i] == target[j]:
                    result[i] = guess[i].lower()
                    target_used[j] = True
                    break

    return "".join(result)


def main() -> None:
    """Executes the core solving pipeline by processing inputs and printing matching candidate words."""
    # 1. Load the input word list
    dictionary = read_dictionary()

    # 2. Parse the history of attempts
    try:
        num_guesses = int(input().strip())
    except ValueError:
        return

    guesses: List[str] = []
    responses: List[str] = []

    for _ in range(num_guesses):
        guesses.append(input().strip())
        responses.append(input().strip())

    # 3. Filter dictionary for words that satisfy all constraints
    matching_answers: List[str] = []

    for word in dictionary:
        is_valid_candidate = True
        for i in range(num_guesses):
            if compute_response(word, guesses[i]) != responses[i]:
                is_valid_candidate = False
                break
        if is_valid_candidate:
            matching_answers.append(word)

    # 4. Output the sorted potential answers
    matching_answers.sort()
    for valid_word in matching_answers:
        print(valid_word)


if __name__ == "__main__":
    main()
