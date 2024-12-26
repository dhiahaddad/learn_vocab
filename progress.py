from dataclasses import dataclass
from typing import List


@dataclass
class Progress:
    words_in_db: int
    studied_words: int
    current_word_lvl: int
    words_in_lvl: List[int]
