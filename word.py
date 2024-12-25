from dataclasses import dataclass
from typing import Tuple

MAX_LVL = 5

@dataclass
class Word:
    id: str
    level: str
    article: str
    deutsch: str
    plural: str
    english: str
    sample_phrase: str
    id2: str
    learned_lvl: str
    correct_translations: str
    correct_articles: str
    incorrect_translations: str
    incorrect_articles: str

    @classmethod
    def from_tuple(
        cls,
        word: Tuple[str, str, str, str, str, str, str, str, str, str, str, str, str],
    ):
        return cls(*word)
