# prose-tokenizer

Lightweight, deterministic, dependency-free Python library for tokenizing English prose and Markdown into blocks, paragraphs, sentences, words, and structural metrics.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`prose-tokenizer` is built for writing tools, LLM preprocessing, readability tools, and lightweight text analysis where consistency and speed are more important than complex NLP models.

## Features

- **Deterministic**: Rule-based logic ensures the same output every time.
- **Markdown-Aware**: Correctly segments headings, list items, and blockquotes.
- **Smart Sentence Splitting**: Handles prefix abbreviations (Mr., Dr.), acronyms (U.S.A.), and decimals (10.5) without breaking sentences.
- **Structure Analysis**: Access text at the block, paragraph, sentence, or word level.
- **Character Metrics**: Total characters, non-whitespace characters, and alphanumeric counts.
- **Zero Dependencies**: Pure Python with no runtime requirements.
- **Fully Typed**: Built with PEP 484 type hints.

## Installation

```bash
pip install prose-tokenizer
```

## Quick Start

```python
from prose_tokenizer import tokenize

content = """
### Q1 Review
The U.S.A. economy grew by 2.5% in Q1. 

*   Growth was driven by tech.
*   Inflation remains stable at 2.1%.
"""

doc = tokenize(content)

print(doc.counts.word_count)     # 20
print(doc.blocks[0].kind)        # "heading"
print(doc.sentences[1])          # "The U.S.A. economy grew by 2.5% in Q1."
```

## What it handles
- **Markdown structural elements**: Headings (# and Setext), list items (*, -, +, 1.), blockquotes (>).
- **English prose heuristics**: Initials (J.R.R. Tolkien), common abbreviations (Jan., etc., vs.), and prefix titles (Dr., Rev.).
- **Complex word tokens**: Contractions (can't), hyphenated words (high-tech), and numbers with commas (1,000) or decimals (2.5).

## What it is not
- **Not a full NLP suite**: Does not perform POS tagging, NER, or dependency parsing. Use spaCy or NLTK for those.
- **Not multi-lingual**: Optimized specifically for English prose.
- **Not AI-powered**: Uses deterministic rules and regular expressions, not machine learning models.

## Use Cases
- **LLM Preprocessing**: Chunking text into logical paragraphs or sentences for RAG or context windows.
- **Writing Tools**: Real-time statistics for word count, sentence length, and readability metrics.
- **Clean Text Extraction**: Removing Markdown noise while preserving structural context.

## API Overview

### `tokenize(text: str) -> TokenizedDocument`
Full analysis of the input text. Returns a dataclass containing `blocks`, `paragraphs`, `sentences`, `words`, and `counts`.

### `split_sentences(text: str) -> List[str]`
Returns a list of sentences, protecting abbreviations and acronyms.

### `split_words(text: str) -> List[str]`
Returns a list of lowercase words, preserving contractions and hyphenation.

### `get_character_metrics(text: str) -> CharacterMetrics`
Calculates total length, length without spaces, and alphanumeric letter counts.

## Development

`prose-tokenizer` uses [Hatch](https://hatch.pypa.io/) for development and builds.

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Linting and Type Checking
ruff check .
mypy .
```

## Release Checklist
1. Update version in `pyproject.toml` and `prose_tokenizer/__init__.py`.
2. Update `CHANGELOG.md`.
3. Run full test suite: `pytest && ruff check . && mypy .`.
4. Build package: `python -m build`.
5. Check distribution: `twine check dist/*`.
6. Upload to PyPI: `twine upload dist/*`.

## License

MIT © [Veldica](https://veldica.com)
