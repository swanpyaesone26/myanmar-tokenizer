"""
Myanmar Tokenizer - Syllable and word segmentation for Myanmar text.

A Python library for segmenting Myanmar (Burmese) text into syllables and words.
Provides two main functions:
- segment_syllables(): Break text into individual syllables
- segment_words(): Intelligently segment text into words using Viterbi algorithm

Example:
    >>> from myanmar_tokenizer import segment_syllables, segment_words
    >>> 
    >>> text = "မြန်မာစာ"
    >>> 
    >>> # Syllable segmentation
    >>> segment_syllables(text)
    'မ ြ န ် မ ာ စ ာ'
    >>> 
    >>> # Word segmentation
    >>> segment_words(text)
    ['မြန်မာ', 'စာ']
"""

__version__ = "1.0.0"
__author__ = "Swan Pyae Sone"
__email__ = "joyboyop69@gmail.com"
__license__ = "MIT"

from .segmentation import segment_syllables, segment_words

__all__ = [
    "segment_syllables",
    "segment_words",
]
