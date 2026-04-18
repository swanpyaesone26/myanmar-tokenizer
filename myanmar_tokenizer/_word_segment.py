"""
Internal word segmentation module using Viterbi algorithm.

This code is an updated version of: https://gist.github.com/markdtw/e2a4e2ee7cef8ea6aed33bb47a97fba6

Updated by Ye Kyaw Thu, LST, NECTEC, Thailand:
- Added recursion limit
- Changed P_unigram and P_bigram as module level global variables
- Using binary ngram dictionaries
- Last Updated: 5 Sept 2021

References:
- Python implementation of Viterbi algorithm for word segmentation
- Updated version: https://gist.github.com/markdtw/e2a4e2ee7cef8ea6aed33bb47a97fba6
- Clean-up of: http://norvig.com/ngrams/ch14.pdf
- Recursion limit: https://www.geeksforgeeks.org/python-handling-recursion-limit/
- A. Viterbi, "Error bounds for convolutional codes and an asymptotically optimum 
  decoding algorithm," in IEEE Transactions on Information Theory, vol. 13, no. 2, 
  pp. 260-269, April 1967
"""

import math
import functools
import sys
import pickle

sys.setrecursionlimit(10**6)

# Module-level global variables
P_unigram = None
P_bigram = None


def read_dict(fileDICT):
    """
    Read binary dictionary file.
    
    Args:
        fileDICT (str): Path to binary dictionary file
        
    Returns:
        dict: Dictionary of ngrams and their counts
    """
    try:
        with open(fileDICT, 'rb') as input_file:
            dictionary = pickle.load(input_file)
            input_file.close()
    except FileNotFoundError:
        print('Dictionary file', fileDICT, ' not found!')
        return {}
    return dictionary


class ProbDist(dict):
    """Probability distribution estimated from unigram/bigram data."""
    
    def __init__(self, datafile=None, unigram=True, N=102490):
        """
        Initialize probability distribution from file.
        
        Args:
            datafile (str): Path to binary dictionary file
            unigram (bool): Whether this is unigram (True) or bigram (False) data
            N (int): Total count for normalization
        """
        data = read_dict(datafile)
        for k, c in data.items():
            self[k] = self.get(k, 0) + c

        if unigram:
            self.unknownprob = lambda k, N: 10/(N*10**len(k))  # Avoid unknown long word
        else:
            self.unknownprob = lambda k, N: 1/N

        self.N = N

    def __call__(self, key):
        """Get probability of key."""
        if key in self:
            return self[key]/self.N
        else:
            return self.unknownprob(key, self.N)


def conditionalProb(word_curr, word_prev):
    """
    Calculate conditional probability of current word given previous word.
    
    Args:
        word_curr (str): Current word
        word_prev (str): Previous word
        
    Returns:
        float: Conditional probability
    """
    try:
        return P_bigram[word_prev + ' ' + word_curr]/P_unigram[word_prev]
    except (KeyError, TypeError):
        return P_unigram(word_curr)


@functools.lru_cache(maxsize=2**10)
def viterbi(text, prev='<S>', maxlen=20):
    """
    Segment text into words using Viterbi algorithm.
    
    Args:
        text (str): Myanmar text to segment
        prev (str): Previous word token (default: '<S>' for start)
        maxlen (int): Maximum word length to consider (default: 20)
        
    Returns:
        tuple: (score, [word_list]) - log probability score and list of segmented words
        
    Example:
        >>> score, words = viterbi("မြန်မာစာ")
        >>> words
        ['မြန်မာ', 'စာ']
    """
    if not text:
        return 0.0, []
    
    textlen = min(len(text), maxlen)
    splits = [(text[:i + 1], text[i + 1:]) for i in range(textlen)]

    candidates = []
    for first_word, remain_word in splits:
        first_prob = math.log10(conditionalProb(first_word, prev))
        remain_prob, remain_word = viterbi(remain_word, first_word)
        candidates.append((first_prob + remain_prob, [first_word] + remain_word))
        
    return max(candidates)
