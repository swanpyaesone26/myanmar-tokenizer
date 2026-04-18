"""
Main segmentation API for myanmar-tokenizer.

Provides simple, user-friendly functions for Myanmar text segmentation.
"""

import os
import sys
from pathlib import Path

from . import _syl_segment
from . import _word_segment


# Auto-load dictionary files on module import
_PACKAGE_DIR = Path(__file__).parent
_DATA_DIR = _PACKAGE_DIR / "data"
_UNIGRAM_FILE = _DATA_DIR / "unigram-word.bin"

_dictionaries_loaded = False


def _load_dictionaries():
    """
    Load unigram and bigram dictionaries for word segmentation.
    
    This function is called automatically on first use of segment_words().
    Lazy loading ensures dictionaries are only loaded when needed.
    """
    global _dictionaries_loaded
    
    if _dictionaries_loaded:
        return
    
    if not _UNIGRAM_FILE.exists():
        raise FileNotFoundError(
            f"Dictionary file not found: {_UNIGRAM_FILE}\n"
            "Please ensure the package data files are properly installed."
        )
    
    # Load unigram dictionary
    _word_segment.P_unigram = _word_segment.ProbDist(str(_UNIGRAM_FILE), unigram=True)
    
    # Load bigram dictionary if it exists, otherwise use only unigram
    _BIGRAM_FILE = _DATA_DIR / "bigram-word.bin"
    if _BIGRAM_FILE.exists():
        _word_segment.P_bigram = _word_segment.ProbDist(str(_BIGRAM_FILE), unigram=False)
    else:
        # Fallback: use unigram for bigram if bigram file not found
        _word_segment.P_bigram = _word_segment.P_unigram
    
    _dictionaries_loaded = True


def segment_syllables(text, delimiter=' '):
    """
    Segment Myanmar text into syllables.
    
    Breaks Myanmar text at syllable/character boundaries. This is useful for
    phonetic analysis or character-level processing.
    
    Args:
        text (str): Myanmar text to segment
        delimiter (str): Delimiter to use between syllables (default: space)
        
    Returns:
        str: Segmented text with delimiter between syllables
        
    Example:
        >>> segment_syllables("မြန်မာစာ")
        'မ ြ န ် မ ာ စ ာ'
        
        >>> segment_syllables("မြန်မာစာ", delimiter='|')
        'မ|ြ|န|်|မ|ာ|စ|ာ'
    """
    return _syl_segment.syllable(text, delimiter=delimiter)


def segment_words(text):
    """
    Segment Myanmar text into words using Viterbi algorithm.
    
    Intelligently segments Myanmar text into words based on unigram/bigram
    probability distributions. This is useful for NLP tasks, document analysis,
    and text processing.
    
    The dictionaries are automatically loaded on first call.
    
    Args:
        text (str): Myanmar text to segment
        
    Returns:
        list: List of segmented words
        
    Raises:
        FileNotFoundError: If dictionary files cannot be found
        
    Example:
        >>> segment_words("မြန်မာစာ")
        ['မြန်မာ', 'စာ']
    """
    _load_dictionaries()
    score, words = _word_segment.viterbi(text)
    return words
