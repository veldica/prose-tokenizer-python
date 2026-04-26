# Prose Tokenizer Python: AI Maintenance Guide

This guide defines the rules and logic for the `prose-tokenizer` Python project. All future AI agents must follow these standards.

## 1. Core Rules

### 1.1 Sentence Splitting
The library uses two sets of short forms to split sentences correctly:
- **High-Confidence Titles**: Words like `Mr.`, `Dr.`, and `Rev.`. These always merge with the next capitalized word.
- **Acronyms and Months**: Words like `U.S.A.` and `Jan.`. These use context to split:
    - **SPLIT** if a common sentence starter follows (like `He`, `It`, `They`).
    - **MERGE** if other capitalized words follow (like `U.S.A. forces`).

### 1.2 Word Logic
The `WORD_REGEX` in `prose_tokenizer/words.py` must:
- Keep commas in numbers (`1,000`).
- Keep dots in decimals (`2.5`).
- Keep dots in acronyms (`U.S.A.`).
- Keep hyphens and short forms.

### 1.3 Markdown Rules
Quotes must be cleaned by removing extra `>` markers from the start of lines.

## 2. Setup

### 2.1 Modules
The package has these parts:
- `prose_tokenizer.words`
- `prose_tokenizer.sentences`
- `prose_tokenizer.paragraphs`
- `prose_tokenizer.markdown`
- `prose_tokenizer.utils`
- `prose_tokenizer.types`

### 2.2 Metrics
The `letter_count` must include both letters and numbers (`[a-zA-Z0-9]`).

## 3. Standards
- **Testing**: Test every change with `pytest`. Add new edge cases to `tests/test_tokenizer.py`.
- **Typing**: Use clear Python type hints everywhere.
- **Builds**: Use `hatchling` to build the package.
