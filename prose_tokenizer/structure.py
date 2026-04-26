"""
Core structure and orchestration for prose tokenization.
"""

from typing import List, Union

from .markdown import get_line_metadata
from .paragraphs import split_paragraph_blocks
from .sentences import split_sentences_from_blocks
from .types import StructureCounts, TokenizedDocument
from .utils import get_character_metrics
from .words import split_words


def count_headings(input_data: Union[str, List[str]]) -> int:
    """Returns the number of headings found in the input text or lines."""
    return get_line_metadata(input_data)["heading_count"]


def count_list_items(input_data: Union[str, List[str]]) -> int:
    """Returns the number of list items found in the input text or lines."""
    return get_line_metadata(input_data)["list_item_count"]


def count_blockquotes(input_data: Union[str, List[str]]) -> int:
    """Returns the number of blockquote blocks found in the input text or lines."""
    return get_line_metadata(input_data)["blockquote_count"]


def get_structure_counts(text: str) -> StructureCounts:
    """
    Returns detailed structural and character counts for the given text
    without returning the full tokenized arrays.
    """
    tokenized = tokenize(text)
    return tokenized.counts


def tokenize(text: str) -> TokenizedDocument:
    """
    Primary entry point for tokenizing English prose and Markdown.

    This function analyzes the input text and returns a TokenizedDocument
    containing hierarchical structure (blocks), paragraphs, sentences,
    individual word tokens, and comprehensive metrics.

    Args:
        text: The raw prose or Markdown string to tokenize.

    Returns:
        A TokenizedDocument object containing all structural data and counts.
    """
    blocks = split_paragraph_blocks(text)
    paragraphs = [block.text for block in blocks]
    sentences = split_sentences_from_blocks(blocks)
    words = split_words(text)

    char_metrics = get_character_metrics(text)

    # Efficiency: Aggregate counts from already parsed blocks where possible
    heading_count = 0
    list_item_count = 0
    blockquote_count = 0

    for block in blocks:
        if block.kind == "heading":
            heading_count += 1
        elif block.kind == "list_item":
            list_item_count += 1
        elif block.kind == "blockquote":
            blockquote_count += 1

    return TokenizedDocument(
        blocks=blocks,
        paragraphs=paragraphs,
        sentences=sentences,
        words=words,
        counts=StructureCounts(
            word_count=len(words),
            sentence_count=len(sentences),
            paragraph_count=len(blocks),
            heading_count=heading_count,
            list_item_count=list_item_count,
            blockquote_count=blockquote_count,
            character_count=char_metrics.character_count,
            character_count_no_spaces=char_metrics.character_count_no_spaces,
            letter_count=char_metrics.letter_count,
        ),
    )


def tokenize_prose(text: str) -> TokenizedDocument:
    """Alias for tokenize."""
    return tokenize(text)
