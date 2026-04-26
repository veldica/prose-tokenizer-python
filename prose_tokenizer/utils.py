"""
Utility functions for text metrics and stopword filtering.
"""

import re

from .types import CharacterMetrics

# Set of common English stopwords for filtering.
STOPWORDS = {
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "can",
    "will",
    "just",
    "don",
    "should",
    "now",
}

STOPWORD_NORM_REGEX = re.compile(r"[^a-z0-9]")
WHITESPACE_REGEX = re.compile(r"\s")
# Mandate: letter_count must include both letters and numbers ([a-zA-Z0-9])
NON_ALPHANUM_REGEX = re.compile(r"[^a-zA-Z0-9]")


def is_stopword(word: str) -> bool:
    """
    Checks if a word is a common English stopword.
    Normalized to lowercase and alphanumeric only before check.
    """
    normalized = STOPWORD_NORM_REGEX.sub("", word.lower())
    return normalized in STOPWORDS


def get_character_metrics(text: str) -> CharacterMetrics:
    """
    Calculates basic character metrics for a string.

    Includes:
    - character_count: Total length including whitespace.
    - character_count_no_spaces: Length excluding all whitespace characters.
    - letter_count: Count of alphanumeric characters ([a-zA-Z0-9]).
    """
    return CharacterMetrics(
        character_count=len(text),
        character_count_no_spaces=len(WHITESPACE_REGEX.sub("", text)),
        letter_count=len(NON_ALPHANUM_REGEX.sub("", text)),
    )
