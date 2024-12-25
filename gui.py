from typing import List
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

from gui_widgets import GroupBox, PushButton, InputField, OutputField, Statistics


class MainWindow(QWidget):
    resetDictButtonClicked = pyqtSignal()
    resetProgressButtonClicked = pyqtSignal()
    submitButtonClicked = pyqtSignal(str, int)
    neverReaskButtonClicked = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Vocabulary Learner")
        self.setGeometry(100, 100, 1000, 600)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 1)

        test_widget = GroupBox(self)
        response_widget = GroupBox(self)

        topHBoxLayout = QHBoxLayout()
        topHBoxLayout.addWidget(test_widget, 1)
        topHBoxLayout.addWidget(response_widget, 1)
        left_layout.addLayout(topHBoxLayout)

        element_height = int(self.height() * 0.2)
        font_size = int(element_height * 0.1)
        label_font = QFont("Sanserif", font_size)
        button_font = QFont("Sanserif", font_size)
        button_font.setBold(True)
        button_font.setFamily("Arial")

        self.__original_word = OutputField(
            "Original word", label_font, element_height, parent=self
        )
        test_widget.addWidget(self.__original_word)

        self.__input_field = InputField(
            "Enter your text here", label_font, element_height, parent=self
        )
        self.__input_field.input_field.returnPressed.connect(self.__submit_input)
        test_widget.addWidget(self.__input_field)

        self.__words_number = InputField(
            "Number of words to be randomized", label_font, element_height, parent=self
        )
        left_layout.addWidget(self.__words_number)

        self.__submitted_word = OutputField(
            "Submitted word", label_font, element_height, parent=self
        )
        response_widget.addWidget(self.__submitted_word)

        self.__translated_word = OutputField(
            "Translated word", label_font, element_height, parent=self
        )
        response_widget.addWidget(self.__translated_word)

        self.__never_reask_button = PushButton(
            "I learned this word. Don't ask again", button_font, element_height, parent=self
        )
        self.__never_reask_button.clicked.connect(self.__never_reask)
        response_widget.addWidget(self.__never_reask_button)

        self.__submit_button = PushButton("Submit", button_font, element_height, parent=self)
        self.__submit_button.clicked.connect(self.__submit_input)
        test_widget.addWidget(self.__submit_button)

        reset_layout = QHBoxLayout()
        left_layout.addLayout(reset_layout)

        self.__reset_dict_button = PushButton(
            "Reload dictionary", button_font, element_height, parent=self
        )
        self.__reset_dict_button.clicked.connect(self.__reset_dict_button_clicked)
        reset_layout.addWidget(self.__reset_dict_button)

        self.__reset_progress_button = PushButton(
            "Reset progress", button_font, element_height, parent=self
        )
        self.__reset_progress_button.clicked.connect(self.__reset_progress_button_clicked)
        reset_layout.addWidget(self.__reset_progress_button)

        self.__statistics = Statistics(label_font, element_height, self)
        right_layout.addWidget(self.__statistics)

        self.setLayout(main_layout)

    def set_original_word(self, word: str) -> None:
        self.__original_word.setText(word)

    def set_translated_word(self, word: str) -> None:
        self.__translated_word.setText(word)

    def set_submitted_word(self, word: str, correct: bool) -> None:
        self.__submitted_word.setText(word)
        if correct:
            self.__submitted_word.value.setStyleSheet("background-color: lime")
        else:
            self.__submitted_word.value.setStyleSheet("background-color: tomato")

    def set_words_number(self, number: int) -> None:
        self.__words_number.setText(str(number))
    
    def set_statistics(self, words_in_db: int, studied_words: int, current_word_lvl: int, words_in_lvl: List[int]) -> None:
        self.__statistics.set_words_in_db(words_in_db)
        self.__statistics.set_studied_words(studied_words)
        self.__statistics.set_current_word_lvl(current_word_lvl)
        self.__statistics.set_words_in_lvl(words_in_lvl)

    def __submit_input(self) -> None:
        input_text = self.__input_field.text()
        words_number = int(self.__words_number.text())
        self.__submitted_word.setText(input_text)
        self.submitButtonClicked.emit(input_text, words_number)
        self.__input_field.input_field.clear()

    def __never_reask(self) -> None:
        self.neverReaskButtonClicked.emit()
        self.__input_field.input_field.clear()

    def __reset_dict_button_clicked(self) -> None:
        self.resetDictButtonClicked.emit()

    def __reset_progress_button_clicked(self) -> None:
        self.resetProgressButtonClicked.emit()
