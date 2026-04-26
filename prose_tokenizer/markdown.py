"""
Low-level Markdown structural analysis.
"""

import re
from typing import Dict, List, Optional, Union

HEADING_REGEX = re.compile(r"^#{1,6}\s+\S.+$")
LIST_ITEM_REGEX = re.compile(r"^[\s\t]*([-*+]|\d+[.)])\s+\S.+$")
BLOCKQUOTE_REGEX = re.compile(r"^[\s\t]*>\s*.+$")
INDENTED_CONTINUATION_REGEX = re.compile(r"^\s{2,}\S")
SETEXT_HEADING_REGEX = re.compile(r"^\s{0,3}(=+|-+)\s*$")


def normalize_lines(text: str) -> List[str]:
    """Normalizes line endings and splits text into a list of lines."""
    return text.replace("\r\n", "\n").split("\n")


def is_heading(line: str) -> bool:
    """Checks if a line is an ATX heading (e.g., # Heading)."""
    return bool(HEADING_REGEX.match(line.strip()))


def is_list_item(line: str) -> bool:
    """Checks if a line starts a list item."""
    return bool(LIST_ITEM_REGEX.match(line.strip()))


def is_blockquote(line: str) -> bool:
    """Checks if a line starts or continues a blockquote."""
    return bool(BLOCKQUOTE_REGEX.match(line.strip()))


def is_indented_continuation(line: str) -> bool:
    """Checks if a line is an indented continuation of a previous block."""
    return bool(INDENTED_CONTINUATION_REGEX.match(line))


def is_setext_heading_line(line: str, next_line: Optional[str] = None) -> bool:
    """Checks if a line followed by a setext underline is a heading."""
    if not line.strip() or not next_line:
        return False
    return bool(SETEXT_HEADING_REGEX.match(next_line.strip()))


def get_line_metadata(input_data: Union[str, List[str]]) -> Dict[str, int]:
    """
    Returns counts of Markdown structural elements.
    Note: For blockquotes, it counts consecutive blockquote lines as a single block.
    """
    lines = normalize_lines(input_data) if isinstance(input_data, str) else input_data
    heading_count = 0
    list_item_count = 0
    blockquote_count = 0

    index = 0
    while index < len(lines):
        current = lines[index].strip() if index < len(lines) else ""
        next_line = lines[index + 1].strip() if index + 1 < len(lines) else None

        if is_heading(current):
            heading_count += 1

        if is_list_item(current):
            list_item_count += 1

        prev = lines[index - 1].strip() if index > 0 else ""
        if is_blockquote(current) and not is_blockquote(prev):
            blockquote_count += 1

        if current and next_line and SETEXT_HEADING_REGEX.match(next_line):
            heading_count += 1
            index += 1

        index += 1

    return {
        "heading_count": heading_count,
        "list_item_count": list_item_count,
        "blockquote_count": blockquote_count,
    }
