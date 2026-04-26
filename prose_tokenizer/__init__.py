"""
Prose Tokenizer: High-precision prose and Markdown tokenization.
"""

from .paragraphs import split_paragraphs
from .sentences import split_sentences
from .structure import (
    count_blockquotes,
    count_headings,
    count_list_items,
    get_structure_counts,
    tokenize,
    tokenize_prose,
)
from .types import (
    CharacterMetrics,
    ParagraphBlock,
    ParagraphBlockKind,
    StructureCounts,
    TokenizedDocument,
)
from .utils import get_character_metrics, is_stopword
from .words import split_words

__version__ = "1.0.0"

__all__ = [
    "tokenize",
    "tokenize_prose",
    "get_structure_counts",
    "count_headings",
    "count_list_items",
    "count_blockquotes",
    "split_sentences",
    "split_paragraphs",
    "split_words",
    "is_stopword",
    "get_character_metrics",
    "TokenizedDocument",
    "StructureCounts",
    "CharacterMetrics",
    "ParagraphBlock",
    "ParagraphBlockKind",
]
