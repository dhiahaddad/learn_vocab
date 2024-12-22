from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from gui_widgets import InOutField, PushButton


class MainWindow(QWidget):
    resetButtonClicked = pyqtSignal()
    submitButtonClicked = pyqtSignal(str,int)
    neverReaskButtonClicked = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Vocabulary Learner")
        self.setGeometry(100, 100, 600, 600)

        self.__layout = QVBoxLayout()

        element_height = int(self.height() * 0.1)
        font_size = int(element_height * 0.2)
        font = QFont("Sanserif", font_size)

        self.__original_word = InOutField(
            "Original word", font, element_height, readonly=True, parent=self
        )
        self.__layout.addWidget(self.__original_word)

        self.__input_field = InOutField(
            "Enter your text here", font, element_height, parent=self
        )
        self.__input_field.returnPressed.connect(self.__submit_input)
        self.__layout.addWidget(self.__input_field)

        self.__words_number = InOutField(
            "Number of words", font, element_height, parent=self
        )
        self.__layout.addWidget(self.__words_number)

        self.__submitted_word = InOutField(
            "Submitted word", font, element_height, readonly=True, parent=self
        )
        self.__layout.addWidget(self.__submitted_word)

        self.__translated_word = InOutField(
            "Translated word", font, element_height, readonly=True, parent=self
        )
        self.__layout.addWidget(self.__translated_word)

        self.__never_reask_button = PushButton("I learned this word. Don't ask again", font, element_height, parent=self)
        self.__never_reask_button.clicked.connect(self.__never_reask)
        self.__layout.addWidget(self.__never_reask_button)

        self.__submit_button = PushButton("Submit", font, element_height, parent=self)
        self.__submit_button.clicked.connect(self.__submit_input)
        self.__layout.addWidget(self.__submit_button)

        self.__reset_button = PushButton("Reset to default", font, element_height, parent=self)
        self.__reset_button.clicked.connect(self.__reset_button_clicked)
        self.__layout.addWidget(self.__reset_button)

        self.setLayout(self.__layout)

    def set_original_word(self, word: str) -> None:
        self.__original_word.setText(word)

    def set_translated_word(self, word: str) -> None:
        self.__translated_word.setText(word)

    def set_submitted_word(self, word: str, correct: bool) -> None:
        self.__submitted_word.setText(word)
        if correct:
            self.__submitted_word.setStyleSheet("background-color: lime")
        else:
            self.__submitted_word.setStyleSheet("background-color: tomato")

    def set_words_number(self, number: int) -> None:
        self.__words_number.setText(str(number))

    def __submit_input(self) -> None:
        input_text = self.__input_field.text()
        words_number = int(self.__words_number.text())
        self.__submitted_word.setText(input_text)
        self.submitButtonClicked.emit(input_text, words_number)
        self.__input_field.clear()

    def __never_reask(self) -> None:
        self.neverReaskButtonClicked.emit()
        self.__input_field.clear()

    def __reset_button_clicked(self) -> None:
        self.resetButtonClicked.emit()
