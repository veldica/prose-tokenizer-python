from prose_tokenizer import (
    __version__,
    get_character_metrics,
    get_structure_counts,
    is_stopword,
    split_paragraphs,
    split_sentences,
    split_words,
    tokenize,
)


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_tokenize_basic() -> None:
    content = """
### Q1 Review
The U.S.A. economy grew by 2.5% in Q1. 

*   Growth was driven by tech.
*   Inflation remains stable at 2.1%.
"""
    doc = tokenize(content)

    # U.S.A. is 1 word, so count is 20
    assert doc.counts.word_count == 20
    assert doc.blocks[0].kind == "heading"
    assert doc.sentences[1] == "The U.S.A. economy grew by 2.5% in Q1."
    assert len(doc.blocks) == 4  # Heading, Paragraph, List Item, List Item


def test_tokenize_blockquotes() -> None:
    content = """
> This is a blockquote.
> It has two lines.
>   > Nested markers should also be handled.

Normal paragraph.
"""
    doc = tokenize(content)

    assert doc.counts.blockquote_count == 1
    assert doc.blocks[0].kind == "blockquote"
    # Continuation markers are stripped.
    # The requirement is "removing extra > markers from the start of lines"
    expected = (
        "> This is a blockquote. It has two lines. "
        "Nested markers should also be handled."
    )
    assert doc.blocks[0].text == expected


def test_split_sentences() -> None:
    text = "Dr. Smith went to the U.S.A. with Mr. Jones. It was 10.5 miles away."
    sentences = split_sentences(text)

    assert len(sentences) == 2
    assert sentences[0] == "Dr. Smith went to the U.S.A. with Mr. Jones."
    assert sentences[1] == "It was 10.5 miles away."


def test_split_sentences_edge_cases() -> None:
    # Test abbreviations at end of sentence
    text = "The package was sent to the U.K. It arrived on Jan. 1st."
    sentences = split_sentences(text)
    assert len(sentences) == 2
    assert sentences[0] == "The package was sent to the U.K."

    # Test initials and name-based acronyms
    text = "J.R.R. Tolkien wrote books. Mr. J. Doe is here."
    sentences = split_sentences(text)
    assert len(sentences) == 2
    assert sentences[0] == "J.R.R. Tolkien wrote books."
    assert sentences[1] == "Mr. J. Doe is here."

    # Test spaced initials
    text = "J. R. R. Tolkien wrote books."
    sentences = split_sentences(text)
    assert len(sentences) == 1
    assert sentences[0] == "J. R. R. Tolkien wrote books."


def test_split_words() -> None:
    text = "The high-tech economy grew 2.5% annually. Can't wait!"
    words = split_words(text)

    expected = [
        "the",
        "high-tech",
        "economy",
        "grew",
        "2.5",
        "annually",
        "can't",
        "wait",
    ]
    assert words == expected


def test_is_stopword() -> None:
    assert is_stopword("the") is True
    assert is_stopword("The") is True
    assert is_stopword("Veldica") is False
    assert is_stopword("and") is True


def test_markdown_setext_headings() -> None:
    content = "Main Title\n==========\nSubtitle\n----------\nParagraph here."
    doc = tokenize(content)
    assert doc.counts.heading_count == 2
    assert doc.blocks[0].text == "Main Title"
    assert doc.blocks[1].text == "Subtitle"
    assert doc.blocks[0].kind == "heading"


def test_list_item_segmentation() -> None:
    content = """
1. First item. It has two sentences.
2. Second item.
"""
    doc = tokenize(content)
    assert doc.counts.list_item_count == 2
    # 1. First item. It has two sentences. -> 2 sentences
    # 2. Second item. -> 1 sentence
    assert len(doc.sentences) == 3
    assert doc.sentences[0] == "1. First item."
    assert doc.sentences[1] == "It has two sentences."
    assert doc.sentences[2] == "2. Second item."


def test_character_metrics() -> None:
    text = "Hello World 123!"
    metrics = get_character_metrics(text)
    # Total chars: 16
    # No spaces: 16 - 2 = 14
    # Letters (alphanum): 13 (Hello World 123)
    assert metrics.character_count == 16
    assert metrics.character_count_no_spaces == 14
    assert metrics.letter_count == 13


def test_empty_input() -> None:
    assert tokenize("").sentences == []
    assert split_sentences("   ") == []
    assert split_words("") == []
    assert split_paragraphs("\n\n") == []


def test_structure_counts_convenience() -> None:
    text = "This is a sentence. This is another."
    counts = get_structure_counts(text)
    assert counts.sentence_count == 2
    assert counts.word_count == 7


def test_split_words_comma_numbers() -> None:
    text = "Revenue was 1,000 dollars."
    words = split_words(text)
    assert words == ["revenue", "was", "1,000", "dollars"]


def test_public_exports() -> None:
    import prose_tokenizer

    expected_exports = {
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
    }
    assert set(prose_tokenizer.__all__) == expected_exports


def test_version_matches_pyproject() -> None:
    import pathlib
    import re

    import prose_tokenizer

    pyproject_path = pathlib.Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, encoding="utf-8") as f:
        content = f.read()

    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    assert match is not None, "Could not find version in pyproject.toml"
    pyproject_version = match.group(1)

    assert prose_tokenizer.__version__ == pyproject_version
