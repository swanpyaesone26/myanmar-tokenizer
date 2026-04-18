#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Demo script for Myanmar syllable and word segmentation.

Usage:
    python3 tools/demo_segmentation.py "မြန်မာစာ"

This will:
- use syl_segment.syllable() with a pipe delimiter
- use word_segment.viterbi() with the available unigram/bigram dictionaries
"""

import os
import sys

SCRIPT_ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_ROOT)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from tools import syl_segment, word_segment

DICT_ROOT = os.path.join(ROOT_DIR, 'dict')

UNIGRAM_FILE = os.path.join(DICT_ROOT, 'unigram-word.bin')
BIGRAM_FILE = os.path.join(DICT_ROOT, 'bigram-word.bin')


def demo_syllable(text, delimiter='|'):
    syl_segment.delimiter = delimiter
    return syl_segment.syllable(text)


def demo_word_segmentation(text, unigram_file=UNIGRAM_FILE, bigram_file=BIGRAM_FILE):
    if not os.path.exists(unigram_file) or not os.path.exists(bigram_file):
        raise FileNotFoundError(
            'Dictionary files not found. Expected {} and {}'.format(unigram_file, bigram_file)
        )

    word_segment.P_unigram = word_segment.ProbDist(unigram_file, unigram=True)
    word_segment.P_bigram = word_segment.ProbDist(bigram_file, unigram=False)

    score, segmented = word_segment.viterbi(text)
    return score, segmented


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 tools/demo_segmentation.py "မြန်မာစာ"')
        sys.exit(1)

    text = sys.argv[1].strip()
    print('Input text:')
    print(text)
    print()

    print('Syllable segmentation:')
    print(demo_syllable(text, delimiter='|'))
    print()

    print('Word segmentation:')
    try:
        score, segmented = demo_word_segmentation(text)
        print('Score:', score)
        print('Result:', ' '.join(segmented))
    except Exception as exc:
        print('Word segmentation failed:', exc)


if __name__ == '__main__':
    main()
