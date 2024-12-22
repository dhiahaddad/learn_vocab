import sys
import os

from dataclasses import dataclass
from typing import Tuple
from PyQt5.QtWidgets import QApplication

from csv_reader import CsvReader
from databse_handler import DatabaseHandler
from gui import MainWindow


@dataclass
class Config:
    spreadsheet_url: str
    test_url: str
    test_path: str
    table_name: str
    db_name: str


@dataclass
class Word:
    id: str
    level: str
    article: str
    deutsch: str
    plural: str
    english: str
    sample_phrase: str

    @classmethod
    def from_tuple(cls, word: Tuple[str, str, str, str, str, str, str]):
        return cls(*word)


class Main:
    __current_word: Word

    def __init__(self, config: Config) -> None:
        self.__config = config

        # if os.path.exists(config.db_name):
        #     os.remove(config.db_name)

        self.__db = DatabaseHandler(config.db_name)
        self.__app = QApplication(sys.argv)
        self.__main_window = MainWindow()

        if not self.__db.table_exists(config.table_name):
            self.__reset_to_default()
        elif self.__db.get_random_row(self.__config.table_name) is None:
            self.__reset_to_default()

    def run(self) -> None:
        self.__main_window.show()

        self.__main_window.resetButtonClicked.connect(self.__reset_to_default)
        self.__main_window.submitButtonClicked.connect(self.__on_submitted)

        self.__load_new_word()

        try:
            sys.exit(self.__app.exec_())
        finally:
            self.__cleanup()

    def __load_new_word(self) -> None:
        random_word = self.__db.get_random_row(self.__config.table_name)
        self.__current_word = Word.from_tuple(random_word)
        self.__main_window.set_original_word(self.__current_word.deutsch)

    def __reset_to_default(self) -> None:
        reader = CsvReader()
        data = reader.read_from_file(config.test_path)
        self.__db.initialize_db_by_df(config.table_name, data)
        self.__db.insert_df_into_db(config.table_name, data)

    def __on_submitted(self, input_text: str) -> None:
        self.__main_window.set_translated_word(self.__current_word.english)
        result = self.__check_answer(input_text)
        self.__main_window.set_submitted_word(input_text, result)
        self.__db.update_progress(self.__config.table_name, self.__current_word.id, result, result)
        self.__load_new_word()

    def __check_answer(self, input_text: str) -> bool:
        if input_text == self.__current_word.english:
            return True
        else:
            return False

    def __cleanup(self) -> None:
        self.__db.close()


config = Config(
    spreadsheet_url="https://docs.google.com/spreadsheets/d/e/2PACX-1vRW9I6TdJPrc-ow1rdZO_p3_ApEK-W47aA9IwIipDNxFITxX4KaJUx5KG79MIK-XxkDHoIQNuOt5ybq/pub?gid=0&single=true&output=csv",
    test_url="https://docs.google.com/spreadsheets/d/e/2PACX-1vTNAXHYCvnJYyVCNdPCF5JQRclv-RzW3oNvYhrHn6_QdgtIGOV3-AvNPeyWSJn7d4jAWNGWDfsUwY9t/pub?gid=0&single=true&output=csv",
    test_path="test.csv",
    table_name="de_en_vocabulary",
    db_name="learn_language.db",
)

main = Main(config)
main.run()
