import os

from dataclasses import dataclass
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from csv_reader import CsvReader
from databse_handler import DatabaseHandler
from progress import Progress
from word import MAX_LVL, Word


@dataclass
class Config:
    spreadsheet_url: str
    test_url: str
    test_path: str
    table_name: str
    db_name: str


class Worker(QObject):
    _current_word: Word
    reset_to_default_started = pyqtSignal()
    reset_to_default_finished = pyqtSignal()

    def __init__(self, config: Config) -> None:
        super().__init__()
        self._config = config

        # if os.path.exists(config.db_name):
        #     os.remove(config.db_name)

        self._db = DatabaseHandler(config.db_name)

        self.words_number = 20

        if not self._db.table_exists(config.table_name):
            self.reset_to_default()
        elif self._db.get_random_row(self._config.table_name, 1) is None:
            self.reset_to_default()

        self.reset_to_default_started.connect(self.reset_to_default)

    def load_new_word(self) -> str:
        random_word = self._db.get_random_row(
            self._config.table_name, self.words_number
        )
        self._current_word = Word.from_tuple(random_word)
        return self._current_word.english

    @pyqtSlot()
    def reset_to_default(self) -> None:
        reader = CsvReader()
        data = reader.read_from_file(self._config.spreadsheet_url)
        db = DatabaseHandler(self._config.db_name)
        db.initialize_db_by_df(self._config.table_name, data)
        db.insert_df_into_db(self._config.table_name, data)
        self.reset_to_default_finished.emit()

    def reset_progress(self) -> None:
        self._db.reset_progress(self._config.table_name)
        self.get_progress()

    def update_progress_in_db(self, result: bool):
        self._db.update_progress(
            self._config.table_name, int(self._current_word.id), result, result
        )
        self._db.update_learning_lvl(
            self._config.table_name, self._current_word, result
        )

    def get_translated_word(self):
        if self._current_word.article is not None:
            translated_word = (
                self._current_word.article + " " + self._current_word.deutsch
            )
        else:
            translated_word = self._current_word.deutsch
        return translated_word

    def set_words_number(self, words_number: int):
        self.words_number = words_number

    def never_reask(self) -> None:
        self._db.set_learned_lvl(
            self._config.table_name,
            int(self._current_word.id),
            MAX_LVL,
        )

    def get_current_learned_lvl(self) -> int:
        return int(self._current_word.learned_lvl)

    def check_answer(self, input_text: str) -> bool:
        if self._current_word.article is not None:
            correct_answer = (
                self._current_word.article + " " + self._current_word.deutsch
            )
        else:
            correct_answer = self._current_word.deutsch
        if input_text.lower() == correct_answer.lower():
            return True
        else:
            return False

    def get_progress(self) -> Progress:
        words_in_db = self._db.get_number_of_rows_in_table(self._config.table_name)
        studied_words = self._db.get_number_of_studied_words(self._config.table_name)
        current_word_lvl = int(self._current_word.learned_lvl)
        words_in_lvl = []
        for i in range(MAX_LVL + 1):
            words_in_lvl.append(
                self._db.get_number_of_words_in_lvl(self._config.table_name, i)
            )
        return Progress(words_in_db, studied_words, current_word_lvl, words_in_lvl)

    def cleanup(self) -> None:
        self._db.close()
