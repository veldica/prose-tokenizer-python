from dataclasses import dataclass
from typing import List, Literal

ParagraphBlockKind = Literal["paragraph", "heading", "list_item", "blockquote"]


@dataclass
class ParagraphBlock:
    text: str
    kind: ParagraphBlockKind
    line_start: int
    line_end: int


@dataclass
class CharacterMetrics:
    character_count: int
    character_count_no_spaces: int
    letter_count: int


@dataclass
class StructureCounts(CharacterMetrics):
    word_count: int
    sentence_count: int
    paragraph_count: int
    heading_count: int
    list_item_count: int
    blockquote_count: int


@dataclass
class TokenizedDocument:
    blocks: List[ParagraphBlock]
    paragraphs: List[str]
    sentences: List[str]
    words: List[str]
    counts: StructureCounts
