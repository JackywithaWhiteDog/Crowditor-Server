"""Text preprocessor

This module contains Preprocessor to process splitted tokens.

    Typical usage example:

    from app.utils.preprocessor import Preprocessor

    preprocessor = Preprocessor()
    preprocessor.preprocess(tokens)

"""
import pickle
import pathlib
import re
from functools import reduce

FILE_PATH = pathlib.Path(__file__).parent.resolve()

with open(FILE_PATH / '../data/model/delim.pickle', 'rb') as file:
    DELEMINATORS = pickle.load(file)

EMOJI_PATTERN = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags=re.UNICODE)

FITLER_WORDS = list(map(str,range(10))) + ['$', '%']

def full2half(string: str) -> str:
    """Convert full-width text to half-width one"""
    # ref:https://segmentfault.com/a/1190000006197218
    result = ''
    for char in string:
        num = ord(char)
        if num == 0x3000:
            num = 32
        elif 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        num = chr(num)
        result += num
    return result

class Preprocessor(object):
    """Preprocessor

    Attributes:
        deliminators (list[str])
        emoji_pattern (re.Pattern[str])
        filter_words (list[str])

    """

    def __init__(self,
        deliminators: 'list[str]' = DELEMINATORS,
        emoji_pattern: 're.Pattern[str]' = EMOJI_PATTERN,
        filter_words: 'list[str]' = FITLER_WORDS
    ) -> None:
        self.deliminators = deliminators
        self.emoji_pattern = emoji_pattern
        self.filter_words = filter_words

    def remove_emoji(self, string: str) -> str:
        """Removes emoji from text"""
        return self.emoji_pattern.sub(r'', string)

    def deli(self, string: str) -> str:
        """Replaces deliminators with space"""
        return reduce(lambda x, y: x.replace(y, ' '), self.deliminators, string)

    def further_split(self, doc: 'list[str]') -> 'list[str]':
        """Splits tokens after further preprocessing"""
        return reduce(lambda x, y: x+self.deli(self.remove_emoji(full2half(y))).split(), doc, [])

    def no_filter_word(self, string: str) -> bool:
        """Returns true if string is not empty and does not contain words to filter"""
        return string and not any(f in string for f in self.filter_words)

    def single_process(self, doc: 'list[str]') -> 'list[str]':
        """Preprocess single token"""
        return [s for s in self.further_split(doc) if self.no_filter_word(s)]

    def preprocess(self, doc: 'list[str]|list[list[str]]') -> 'list[str]|list[list[str]]':
        """Preprocess tokens"""

        if not doc:
            return doc

        if isinstance(doc[0], list):
            return [self.single_process(d) for d in doc]

        return self.single_process(doc)
