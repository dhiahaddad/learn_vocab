import sys

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
    level: str
    article: str
    deutsch: str
    plural: str
    english: str
    sample_phrase: str

    @classmethod
    def from_tuple(cls, word: Tuple[str, str, str, str, str, str]):
        return cls(*word)


class Main:
    current_word: Word

    def __init__(self, config: Config) -> None:
        self.config = config
        self.db = DatabaseHandler(config.db_name)
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()

    def run(self) -> None:
        self.main_window.show()

        self.main_window.resetButtonClicked.connect(self.reset_to_default)
        self.main_window.submitButtonClicked.connect(self.on_submitted)

        self.load_new_word()

        try:
            sys.exit(self.app.exec_())
        finally:
            self.cleanup()

    def load_new_word(self) -> None:
        self.current_word = Word.from_tuple(
            self.db.get_random_row(self.config.table_name)
        )
        self.main_window.set_original_word(self.current_word.deutsch)

    def reset_to_default(self) -> None:
        reader = CsvReader()
        data = reader.read_from_file(config.test_path)
        self.db.initialize_db_by_df(config.table_name, data)
        self.db.insert_df_into_db(config.table_name, data)

    def on_submitted(self, input_text: str) -> None:
        self.main_window.set_translated_word(self.current_word.english)
        result = self.check_answer(input_text)
        self.main_window.set_submitted_word(input_text, result)
        self.load_new_word()

    def check_answer(self, input_text: str) -> bool:
        if input_text == self.current_word.english:
            return True
        else:
            return False

    def cleanup(self) -> None:
        self.db.close()


config = Config(
    spreadsheet_url="https://docs.google.com/spreadsheets/d/e/2PACX-1vRW9I6TdJPrc-ow1rdZO_p3_ApEK-W47aA9IwIipDNxFITxX4KaJUx5KG79MIK-XxkDHoIQNuOt5ybq/pub?gid=0&single=true&output=csv",
    test_url="https://docs.google.com/spreadsheets/d/e/2PACX-1vTNAXHYCvnJYyVCNdPCF5JQRclv-RzW3oNvYhrHn6_QdgtIGOV3-AvNPeyWSJn7d4jAWNGWDfsUwY9t/pub?gid=0&single=true&output=csv",
    test_path="test.csv",
    table_name="de_en_vocabulary",
    db_name="learn_language.db",
)

main = Main(config)
main.run()
