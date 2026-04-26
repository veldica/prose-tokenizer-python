from typing import Any

from prose_tokenizer import tokenize


def test_performance_large_document(benchmark: Any) -> None:
    """
    Benchmark the tokenization of a relatively large document
    to ensure regex patterns are efficient.
    """
    base_content = """
### Section Header
The U.S.A. economy grew by 2.5% in Q1. Mr. Smith was very happy about this.
Dr. Jones, however, was skeptical. "It's not that simple," he said.

*   Item 1: Tech growth.
*   Item 2: Inflation at 2.1%.

> Blockquote line 1.
> Blockquote line 2.
"""
    # Create a ~100KB document by repeating the base content
    large_content = base_content * 100

    result = benchmark(tokenize, large_content)

    # Basic sanity check on the result
    assert result.counts.word_count > 0
    assert result.counts.sentence_count > 0


def test_performance_many_acronyms(benchmark: Any) -> None:
    """
    Benchmark a document with many acronyms and abbreviations
    to test the heuristic merging logic.
    """
    content = "U.S.A. " * 500 + "Dr. Smith. " * 500

    result = benchmark(tokenize, content)

    assert result.counts.word_count > 0
