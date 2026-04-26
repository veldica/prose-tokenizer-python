import re
from pathlib import Path

import prose_tokenizer


def test_split_words_comma_numbers() -> None:
    """Task 3: Confirm comma numbers are preserved in word tokenization."""
    from prose_tokenizer import split_words

    assert split_words("Revenue was 1,000 dollars.") == [
        "revenue",
        "was",
        "1,000",
        "dollars",
    ]
    assert "1,234,567.89" in split_words("The value is 1,234,567.89 units.")


def test_public_api_exports() -> None:
    """Task 4: Verify documented public names exist and are in __all__."""
    expected = [
        "tokenize",
        "tokenize_prose",
        "split_sentences",
        "split_paragraphs",
        "split_words",
        "get_character_metrics",
        "get_structure_counts",
        "is_stopword",
        "TokenizedDocument",
        "StructureCounts",
        "CharacterMetrics",
        "ParagraphBlock",
        "ParagraphBlockKind",
    ]
    for name in expected:
        assert hasattr(prose_tokenizer, name), f"{name} not found in prose_tokenizer"
        assert name in prose_tokenizer.__all__, (
            f"{name} not found in prose_tokenizer.__all__"
        )


def test_version_matches_pyproject() -> None:
    """Task 5: Verify prose_tokenizer.__version__ matches pyproject.toml."""
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    content = pyproject.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    assert match is not None
    assert prose_tokenizer.__version__ == match.group(1)


def test_readme_quickstart() -> None:
    """Task 6: Re-confirm README quick-start behavior."""
    from prose_tokenizer import tokenize

    content = """
### Q1 Review
The U.S.A. economy grew by 2.5% in Q1. 

*   Growth was driven by tech.
*   Inflation remains stable at 2.1%.
"""
    doc = tokenize(content)

    assert doc.counts.word_count == 20
    assert doc.blocks[0].kind == "heading"
    assert doc.sentences[1] == "The U.S.A. economy grew by 2.5% in Q1."
