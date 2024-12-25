import sys
import os

from dataclasses import dataclass
from PyQt5.QtWidgets import QApplication

from csv_reader import CsvReader
from databse_handler import DatabaseHandler
from gui import MainWindow
from word import MAX_LVL, Word

os.chdir(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class Config:
    spreadsheet_url: str
    test_url: str
    test_path: str
    table_name: str
    db_name: str


class Main:
    __current_word: Word

    def __init__(self, config: Config) -> None:
        self.__config = config

        # if os.path.exists(config.db_name):
        #     os.remove(config.db_name)

        self.__db = DatabaseHandler(config.db_name)
        self.__app = QApplication(sys.argv)
        self.__words_number = 20
        self.__main_window = MainWindow()
        self.__main_window.set_words_number(self.__words_number)

        if not self.__db.table_exists(config.table_name):
            self.__reset_to_default()
        elif self.__db.get_random_row(self.__config.table_name, 1) is None:
            self.__reset_to_default()

        self.__db.update_rows_number(self.__config.table_name)

    def run(self) -> None:
        self.__main_window.show()

        self.__main_window.resetDictButtonClicked.connect(self.__reset_to_default)
        self.__main_window.resetProgressButtonClicked.connect(self.__reset_progress)
        self.__main_window.submitButtonClicked.connect(self.__on_submitted)
        self.__main_window.neverReaskButtonClicked.connect(self.__on_never_reask)

        self.__load_new_word()

        try:
            sys.exit(self.__app.exec_())
        finally:
            self.__cleanup()

    def __load_new_word(self) -> None:
        random_word = self.__db.get_random_row(
            self.__config.table_name, self.__words_number
        )
        self.__current_word = Word.from_tuple(random_word)
        self.__main_window.set_original_word(self.__current_word.english)
        self.update_statistics()

    def __reset_to_default(self) -> None:
        reader = CsvReader()
        data = reader.read_from_file(config.spreadsheet_url)
        self.__db.initialize_db_by_df(config.table_name, data)
        self.__db.insert_df_into_db(config.table_name, data)
        self.__load_new_word()

    def __reset_progress(self) -> None:
        self.__db.reset_progress(self.__config.table_name)
        self.update_statistics()

    def __on_submitted(self, input_text: str, words_number: int) -> None:
        self.__words_number = words_number
        if self.__current_word.article is not None:
            translated_word = self.__current_word.article + " " + self.__current_word.deutsch
        else:
            translated_word = self.__current_word.deutsch
        self.__main_window.set_translated_word(
            translated_word
        )
        result = self.__check_answer(input_text)
        self.__main_window.set_submitted_word(input_text, result)
        self.__db.update_progress(
            self.__config.table_name, int(self.__current_word.id), result, result
        )
        self.__db.update_learning_lvl(
            self.__config.table_name, self.__current_word, result
        )
        self.__load_new_word()

    def __on_never_reask(self) -> None:
        self.__db.set_learned_lvl(
            self.__config.table_name,
            int(self.__current_word.id),
            MAX_LVL,
        )
        self.__load_new_word()

    def __check_answer(self, input_text: str) -> bool:
        if self.__current_word.article is not None:
            correct_answer = self.__current_word.article + " " + self.__current_word.deutsch
        else:
            correct_answer = self.__current_word.deutsch
        if input_text.lower() == correct_answer.lower():
            return True
        else:
            return False

    def update_statistics(self) -> None:
        words_in_db = self.__db.get_number_of_rows_in_table(self.__config.table_name)
        studied_words = self.__db.get_number_of_studied_words(self.__config.table_name)
        current_word_lvl = self.__current_word.learned_lvl
        words_in_lvl = []
        for i in range(MAX_LVL + 1):
            words_in_lvl.append(
                self.__db.get_number_of_words_in_lvl(self.__config.table_name, i)
            )

        self.__main_window.set_statistics(
            words_in_db, studied_words, current_word_lvl, words_in_lvl
        )

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
