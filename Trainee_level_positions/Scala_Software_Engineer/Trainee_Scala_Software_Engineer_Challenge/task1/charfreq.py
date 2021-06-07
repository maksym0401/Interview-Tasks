from functools import lru_cache
from string import ascii_lowercase
from typing import Dict
from pprint import pformat


ENGLISH_ALPHABET = set(ascii_lowercase)


@lru_cache
def count_chars_frequency(text: str) -> Dict[str, int]:
    '''Takes string and counts frequency of occurrence of
    each character of English alphabet in this string.'''
    freqs = {}
    for char in text:
        char = char.lower()
        if char not in ENGLISH_ALPHABET:
            continue
        freqs[char] = freqs.get(char, 0) + 1

    return freqs


def calc_chars_probabilities(text: str) -> Dict[str, float]:
    '''Takes string and caclulate probability of occurrence of
    each character of English alphabet with double precision in this string.'''
    freqs = count_chars_frequency(text)
    return {
        char: round(count/len(text), 2) for char, count in freqs.items()
    }


def main():
    text = input('Enter text --> ')
    frequencies = count_chars_frequency(text)
    probabilities = calc_chars_probabilities(text)
    print(f'Frequencies:\n {pformat(frequencies)}')
    print(f'Probabilities:\n {pformat(probabilities)}')


if __name__ == '__main__':
    main()
