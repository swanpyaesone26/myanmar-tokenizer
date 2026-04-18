# Myanmar Tokenizer

A Python library for segmenting Myanmar (Burmese) text into syllables and words.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Syllable Segmentation**: Break Myanmar text into individual syllables/characters
- **Word Segmentation**: Intelligently segment Myanmar text into words using the Viterbi algorithm
- **Simple API**: Easy-to-use functions for quick text processing
- **No External Dependencies**: Uses only Python standard library

## Installation

```bash
pip install myanmar-tokenizer
```

## Quick Start

```python
from myanmar_tokenizer import segment_syllables, segment_words

text = "မြန်မာစာ"

# Syllable segmentation
print(segment_syllables(text))
# Output: မ ြ န ် မ ာ စ ာ

# Word segmentation
print(segment_words(text))
# Output: ['မြန်မာ', 'စာ']
```

## Usage

### Syllable Segmentation

Breaks Myanmar text into individual syllables:

```python
from myanmar_tokenizer import segment_syllables

text = "မြန်မာစာ"

# Default: space delimiter
result = segment_syllables(text)
# 'မ ြ န ် မ ာ စ ာ'

# Custom delimiter
result = segment_syllables(text, delimiter='|')
# 'မ|ြ|န|်|မ|ာ|စ|ာ'
```

**Use case**: Phonetic analysis, character-level NLP tasks, text preprocessing.

### Word Segmentation

Intelligently segments Myanmar text into words using probability distributions:

```python
from myanmar_tokenizer import segment_words

text = "မြန်မာစာ"
words = segment_words(text)
# ['မြန်မာ', 'စာ']
```

**Use case**: NLP tasks, text analysis, document processing, machine learning features.

## Algorithm Details

### Syllable Segmentation
- Uses regular expressions based on Myanmar Unicode patterns
- Identifies syllable-initial consonants and splits at appropriate boundaries
- Respects Myanmar-specific character combining rules

### Word Segmentation
- Implements the **Viterbi algorithm** for dynamic programming
- Uses **unigram and bigram probability distributions** from Myanmar text corpus
- Finds the most probable word segmentation path through text
- Maximum word length: 20 characters (configurable)

## Requirements

- Python 3.7 or higher
- No additional dependencies (uses only Python standard library)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Syllable segmentation based on Myanmar Unicode reference
- Word segmentation algorithm by Ye Kyaw Thu and contributions from NLP researchers
- Original Viterbi implementation reference: https://gist.github.com/markdtw/e2a4e2ee7cef8ea6aed33bb47a97fba6

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Special thanks to Ye Kyaw Thu (Waseda University, NECTEC) for the original algorithm implementations.