"""
Sentence segmentation with heuristics for abbreviations and acronyms.
"""

import re
from typing import List, Match

from .paragraphs import split_paragraph_blocks
from .types import ParagraphBlock

# Regex for identifying sentence boundaries while ignoring decimal dots and acronyms.
SENTENCE_BREAK_REGEX = re.compile(
    r'[.!?]+["\'”’)\]]*(?=\s+(?:["\'“‘(]*[A-Z0-9#*_-])|\s*$)'
)
DECIMAL_PROTECT_REGEX = re.compile(r"(\d)\.(\d)")
ACRONYM_REGEX = re.compile(r"\b((?:[A-Za-z]\.){2,})(?=(?:\s|$|[\"')\]]))")
INITIALS_REGEX = re.compile(r"(^|[\s\t(])([A-Z])\.(?=\s+[A-Z])")
LIST_ITEM_BLOCK_REGEX = re.compile(r"^([\s\t]*([-*+]|\d+[.)])\s+)(.*)$")
BLOCKQUOTE_BLOCK_REGEX = re.compile(r"^([\s\t]*>\s+)(.*)$")

DECIMAL_PLACEHOLDER = "\u0000"
INNER_DOT_PLACEHOLDER = "\u0001"
INITIAL_PLACEHOLDER = "\u0002"

PREFIX_ABBREVIATIONS = {
    "mr.",
    "mrs.",
    "ms.",
    "dr.",
    "prof.",
    "sr.",
    "jr.",
    "gen.",
    "adm.",
    "capt.",
    "col.",
    "maj.",
    "sgt.",
    "lt.",
    "st.",
    "rev.",
    "hon.",
    "gov.",
    "pres.",
    "sen.",
    "rep.",
    "mt.",
}

AMBIGUOUS_ABBREVIATIONS = {
    "u.s.",
    "u.k.",
    "u.s.a.",
    "e.g.",
    "i.e.",
    "jan.",
    "feb.",
    "mar.",
    "apr.",
    "jun.",
    "jul.",
    "aug.",
    "sep.",
    "sept.",
    "oct.",
    "nov.",
    "dec.",
    "approx.",
    "avg.",
    "dept.",
    "est.",
    "etc.",
    "fig.",
    "inc.",
    "ltd.",
    "min.",
    "max.",
    "vs.",
}

SENTENCE_STARTERS = {
    "the",
    "a",
    "an",
    "he",
    "she",
    "it",
    "they",
    "we",
    "i",
    "you",
    "this",
    "that",
    "there",
    "who",
    "when",
    "where",
    "while",
    "but",
    "and",
    "if",
    "then",
    "my",
    "our",
    "his",
    "her",
    "their",
}


def split_sentences(text: str) -> List[str]:
    """
    Splits text into a flat list of sentences.
    Processes the text through structural block analysis first to ensure
    Markdown elements are handled correctly.
    """
    if not text.strip():
        return []
    return split_sentences_from_blocks(split_paragraph_blocks(text))


def split_sentences_from_blocks(blocks: List[ParagraphBlock]) -> List[str]:
    """Extracts and splits sentences from a list of ParagraphBlocks."""
    sentences: List[str] = []
    for block in blocks:
        sentences.extend(split_sentences_from_block(block))
    return [s for s in sentences if s]


def split_sentences_from_block(block: ParagraphBlock) -> List[str]:
    """Splits sentences within a specific structural block."""
    if block.kind == "heading":
        return [block.text]

    if block.kind == "list_item":
        match = LIST_ITEM_BLOCK_REGEX.match(block.text)
        if match:
            prefix = match.group(1)
            content = match.group(3)
            item_sentences = _split_sentence_internal(content)
            if item_sentences:
                item_sentences[0] = f"{prefix}{item_sentences[0]}"
                return item_sentences

    if block.kind == "blockquote":
        match = BLOCKQUOTE_BLOCK_REGEX.match(block.text)
        if match:
            prefix = match.group(1)
            content = match.group(2)
            quote_sentences = _split_sentence_internal(content)
            if quote_sentences:
                quote_sentences[0] = f"{prefix}{quote_sentences[0]}"
                return quote_sentences

    return _split_sentence_internal(block.text)


def _split_sentence_internal(text: str) -> List[str]:
    """Internal sentence splitting logic using placeholders and regex."""
    if not text.strip():
        return []

    processed = text
    processed = DECIMAL_PROTECT_REGEX.sub(rf"\1{DECIMAL_PLACEHOLDER}\2", processed)

    def protect_acronyms(match: Match[str]) -> str:
        return re.sub(r"\.(?=.+\.)", INNER_DOT_PLACEHOLDER, match.group(0))

    processed = ACRONYM_REGEX.sub(protect_acronyms, processed)
    processed = INITIALS_REGEX.sub(rf"\1\2{INITIAL_PLACEHOLDER}", processed)

    segments: List[str] = []
    start_index = 0

    for match in SENTENCE_BREAK_REGEX.finditer(processed):
        end_index = match.end()
        candidate = _restore_placeholders(processed[start_index:end_index].strip())
        if candidate:
            segments.append(candidate)

        start_index = end_index
        while start_index < len(processed) and processed[start_index].isspace():
            start_index += 1

    remainder = _restore_placeholders(processed[start_index:].strip())
    if remainder:
        segments.append(remainder)

    return _merge_false_boundaries(segments)


def is_acronym(token: str) -> bool:
    """Checks if a token looks like an acronym (e.g., U.S.A. or J.R.R.)."""
    # Remove trailing punctuation except dot
    t = token.rstrip(")\"']!?.")
    if token.endswith("."):
        t += "."
    return bool(re.match(r"^([a-z]\.)+[a-z]?\.?$", t.lower()))


def _merge_false_boundaries(segments: List[str]) -> List[str]:
    """Heuristic-based merging of segments that were incorrectly split."""
    merged: List[str] = []

    for segment in segments:
        if not merged:
            merged.append(segment)
            continue

        previous = merged[-1]
        prev_tokens = previous.split()
        previous_last_token = prev_tokens[-1].lower() if prev_tokens else ""

        next_tokens = segment.split()
        next_first_token = next_tokens[0] if next_tokens else ""
        next_first_token_lower = next_first_token.lower()

        # 1. Prefix-only abbreviations (Mr., Dr.)
        if previous_last_token in PREFIX_ABBREVIATIONS and re.match(
            r"^[A-Z0-9]", next_first_token
        ):
            merged[-1] = f"{previous} {segment}"
            continue

        # 2. Ambiguous abbreviations (U.S.A., Jan.) and dynamic acronyms
        if (
            previous_last_token in AMBIGUOUS_ABBREVIATIONS
            or is_acronym(previous_last_token)
        ) and (
            next_first_token_lower not in SENTENCE_STARTERS
            and re.match(r"^[A-Z0-9]", next_first_token)
        ):
            merged[-1] = f"{previous} {segment}"
            continue

        merged.append(segment)

    return merged


def _restore_placeholders(value: str) -> str:
    """Reverts internal placeholders back to their original characters."""
    return (
        value.replace(DECIMAL_PLACEHOLDER, ".")
        .replace(INNER_DOT_PLACEHOLDER, ".")
        .replace(INITIAL_PLACEHOLDER, ".")
        .strip()
    )
