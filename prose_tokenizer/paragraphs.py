"""
Structural block analysis for prose and Markdown.
"""

import re
from typing import List, Literal, Optional

from .markdown import (
    is_blockquote,
    is_heading,
    is_indented_continuation,
    is_list_item,
    is_setext_heading_line,
    normalize_lines,
)
from .types import ParagraphBlock, ParagraphBlockKind

BLOCKQUOTE_STRIPPER_REGEX = re.compile(r"^([\s\t]*>\s*)+")


def split_paragraph_blocks(text: str) -> List[ParagraphBlock]:
    """
    Analyzes text and splits it into structural blocks.

    Blocks can be paragraphs, headings, list items, or blockquotes.
    Consecutive lines of the same block type are merged (except headings).
    Markdown markers in blockquotes are cleaned from continuation lines.
    """
    if not text.strip():
        return []

    lines = normalize_lines(text)
    paragraphs: List[ParagraphBlock] = []
    current: List[str] = []
    current_start = -1
    current_end = -1
    mode: Optional[Literal["prose", "list", "blockquote"]] = None

    def flush_current(kind: Optional[ParagraphBlockKind] = None) -> None:
        nonlocal current, mode, current_start, current_end
        if not kind:
            if mode == "list":
                kind = "list_item"
            elif mode == "blockquote":
                kind = "blockquote"
            else:
                kind = "paragraph"

        if not current:
            mode = None
            current_start = -1
            current_end = -1
            return

        paragraphs.append(
            ParagraphBlock(
                text=" ".join(current).strip(),
                kind=kind,
                line_start=current_start,
                line_end=current_end,
            )
        )
        current = []
        mode = None
        current_start = -1
        current_end = -1

    index = 0
    while index < len(lines):
        line = lines[index]
        trimmed = line.strip()

        if not trimmed:
            flush_current()
            index += 1
            continue

        next_line = lines[index + 1] if index + 1 < len(lines) else None
        if is_setext_heading_line(trimmed, next_line):
            flush_current()
            paragraphs.append(
                ParagraphBlock(
                    text=trimmed,
                    kind="heading",
                    line_start=index,
                    line_end=index + 1,
                )
            )
            index += 2
            continue

        if is_heading(trimmed):
            flush_current()
            paragraphs.append(
                ParagraphBlock(
                    text=trimmed,
                    kind="heading",
                    line_start=index,
                    line_end=index,
                )
            )
            index += 1
            continue

        if is_list_item(trimmed):
            flush_current()
            current = [trimmed]
            current_start = index
            current_end = index
            mode = "list"
            index += 1
            continue

        if is_blockquote(trimmed):
            if mode != "blockquote":
                flush_current()
            if not current:
                current_start = index
                current.append(trimmed)
            else:
                # Requirement: Remove extra > markers from the start of lines in
                # blockquotes
                stripped = BLOCKQUOTE_STRIPPER_REGEX.sub("", trimmed)
                current.append(stripped)
            current_end = index
            mode = "blockquote"
            index += 1
            continue

        if mode == "list" and is_indented_continuation(line):
            current.append(trimmed)
            current_end = index
            index += 1
            continue

        if mode != "prose":
            flush_current()
            mode = "prose"

        if not current:
            current_start = index
        current.append(trimmed)
        current_end = index
        index += 1

    flush_current()

    return paragraphs


def split_paragraphs(text: str) -> List[str]:
    """Returns a list of raw paragraph strings from the input text."""
    return [block.text for block in split_paragraph_blocks(text)]
