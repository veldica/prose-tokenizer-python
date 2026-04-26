# prose-tokenizer

[![PyPI Version](https://img.shields.io/pypi/v/prose-tokenizer)](https://pypi.org/project/prose-tokenizer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-blue)](pyproject.toml)

A high-precision, rule-based prose tokenizer and sentence segmentation library for English and Markdown. Designed for accurate splitting of paragraphs, sentences, and words in AI pipelines, LLM context window management, and editorial automation.

`prose-tokenizer` is built for writing tools, LLM preprocessing, readability tools, and lightweight text analysis where consistency and speed are more important than complex, probabilistic NLP models.

## Features

- **Deterministic Rule-Based Engine**: Consistent, predictable output without the overhead or unpredictability of machine learning models.
- **Markdown-Native Support**: Properly handles structural elements including headings (# and Setext), list items (*, -, +, 1.), and blockquotes (>).
- **Intelligent Sentence Segmentation**: Respects English prose heuristics such as prefix titles (Dr., Mr.), acronyms (U.S.A.), initials (J.R.R. Tolkien), and interior decimals.
- **Hierarchical Analysis**: Access text at the block, paragraph, sentence, or word level with a single call.
- **Character Metrics**: Accurate counts for total characters, non-whitespace characters, and alphanumeric letter counts.
- **Zero Dependencies**: Pure Python implementation with no runtime requirements.
- **Fully Typed**: Built with PEP 484 type hints for excellent IDE support.

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

## API Reference

### `tokenize(text: str) -> TokenizedDocument`
The primary entry point for full document analysis. Returns a dataclass containing:
- `blocks`: List of `ParagraphBlock` objects (includes `text`, `kind`, `line_start`, and `line_end`).
- `paragraphs`: List of raw paragraph strings.
- `sentences`: List of sentence strings.
- `words`: List of lowercase word tokens.
- `counts`: `StructureCounts` object with aggregated metrics.

`tokenize_prose` is provided as an alias for this function.

### `split_sentences(text: str) -> List[str]`
Splits prose into a list of sentence strings using deterministic rules that protect abbreviations and decimal numbers.

### `split_paragraphs(text: str) -> List[str]`
Splits text into a list of raw paragraph strings based on double newlines.

### `split_words(text: str) -> List[str]`
Splits text into lowercase alphanumeric word tokens, preserving contractions (e.g., "can't") and interior hyphens or decimals.

### `get_character_metrics(text: str) -> CharacterMetrics`
Calculates character-level statistics:
- `character_count`: Total character length.
- `character_count_no_spaces`: Count excluding whitespace.
- `letter_count`: Count of alphanumeric letters (a-z, A-Z, 0-9).

### `get_structure_counts(text: str) -> StructureCounts`
A convenience function that returns structural metrics without full tokenization arrays. Includes `word_count`, `sentence_count`, `paragraph_count`, `heading_count`, `list_item_count`, and `blockquote_count`.

### `is_stopword(word: str) -> bool`
Checks if a word is a common English stopword.

## Practical Use Cases

- **LLM Preprocessing**: Chunking text into logical paragraphs or sentences for RAG or context window management while preserving Markdown structure.
- **Writing Tools**: Real-time statistics for word count, sentence length, and readability metrics (e.g., Flesch-Kincaid).
- **Clean Text Extraction**: Removing or identifying Markdown noise while preserving structural context.
- **Search Indexing**: Generating clean, lowercase word tokens for search engines.

## Limitations

- **Language Support**: Optimized specifically for English prose.
- **NLP Scope**: Does not perform POS tagging, NER, or dependency parsing.
- **Rule-Based**: While highly accurate, it uses deterministic heuristics rather than probabilistic context analysis.

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

## Ownership & Authority

This package is maintained by **Veldica Research** as a core part of our writing analysis platform. Built for production environments that demand high reliability, precision, and performance.

- **Full Documentation**: [veldica.com/python-prose-tokenizer](https://veldica.com/python-prose-tokenizer)
- **Veldica Platform**: [veldica.com](https://veldica.com)
- **Report Bugs**: [GitHub Issues](https://github.com/veldica/prose-tokenizer-python/issues)

## License

MIT © [Veldica Research](https://veldica.com)
