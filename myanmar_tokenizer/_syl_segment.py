#-*- coding:utf-8 -*- 
"""
Internal syllable segmentation module.

Last updated: 21 July 2016
Written by Ye Kyaw Thu, Visiting Researcher, Waseda University
Homepage: https://sites.google.com/site/yekyawthunlp/

Reference of Myanmar Unicode: http://unicode.org/charts/PDF/U1000.pdf
"""

import re

myConsonant = r"က-အ"
enChar = r"a-zA-Z0-9"
otherChar = r"ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s"
ssSymbol = r'္'
aThat = r'်'

# Regular expression pattern for Myanmar syllable breaking
# A consonant not after a subscript symbol AND a consonant is not followed by 
# a-That character or a subscript symbol
BreakPattern = re.compile(
    r"((?<!" + ssSymbol + r")["+ myConsonant + r"](?![" + aThat + ssSymbol + r"])" + r"|[" + enChar + otherChar + r"])",
    re.UNICODE
)


def syllable(line, delimiter=' '):
    """
    Segment Myanmar text into syllables.
    
    Args:
        line (str): Myanmar text to segment
        delimiter (str): Delimiter to use between syllables (default: space)
        
    Returns:
        str: Segmented text with delimiter between syllables
        
    Example:
        >>> syllable("မြန်မာစာ", delimiter='|')
        'မြန်|မာ|စာ'
    """
    result = BreakPattern.sub(delimiter + r"\1", line)
    return result.lstrip(delimiter)  # Remove leading delimiter
