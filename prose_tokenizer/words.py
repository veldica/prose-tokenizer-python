"""
Word-level tokenization and normalization logic.
"""

import re
from typing import List

# Matches words, contractions, hyphenated words, decimals, and acronyms.
WORD_REGEX = re.compile(
    r"[a-z0-9]+(?:['’][a-z0-9]+|-[a-z0-9]+|\.[a-z0-9]+|,\d+)*", re.IGNORECASE
)
HAS_ALPHANUM_REGEX = re.compile(r"[a-z0-9]")
CLEAN_SUFFIX_REGEX = re.compile(r"[.-]+$")


def split_words(text: str) -> List[str]:
    """
    Splits text into lowercase word tokens.

    Handles complex cases including:
    - Contractions (can't, it's)
    - Hyphenated words (well-being)
    - Decimals (2.5)
    - Numerical commas (1,000)
    - Acronyms (U.S.A.)

    Trailing periods and hyphens are stripped from tokens.
    """
    if not text.strip():
        return []

    matches = WORD_REGEX.findall(text)
    if not matches:
        return []

    words = []
    for word in matches:
        word_lower = word.lower()
        if HAS_ALPHANUM_REGEX.search(word_lower):
            # Strip trailing punctuation often caught by regex in acronyms/decimals
            cleaned = CLEAN_SUFFIX_REGEX.sub("", word_lower)
            words.append(cleaned)

    return words
