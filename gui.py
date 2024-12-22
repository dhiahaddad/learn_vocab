from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

from gui_widgets import GroupBox, PushButton, InputField, OutputField


class MainWindow(QWidget):
    resetButtonClicked = pyqtSignal()
    submitButtonClicked = pyqtSignal(str, int)
    neverReaskButtonClicked = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Vocabulary Learner")
        self.setGeometry(100, 100, 800, 600)

        self.__layout = QVBoxLayout()

        test_widget = GroupBox(self)
        response_widget = GroupBox(self)

        topHBoxLayout = QHBoxLayout()
        topHBoxLayout.addWidget(test_widget, 1)
        topHBoxLayout.addWidget(response_widget, 1)
        self.__layout.addLayout(topHBoxLayout)

        element_height = int(self.height() * 0.2)
        font_size = int(element_height * 0.1)
        font = QFont("Sanserif", font_size)

        self.__original_word = OutputField(
            "Original word", font, element_height, parent=self
        )
        test_widget.addWidget(self.__original_word)

        self.__input_field = InputField(
            "Enter your text here", font, element_height, parent=self
        )
        self.__input_field.input_field.returnPressed.connect(self.__submit_input)
        test_widget.addWidget(self.__input_field)

        self.__words_number = InputField(
            "Number of words to be randomized", font, element_height, parent=self
        )
        self.__layout.addWidget(self.__words_number)

        self.__submitted_word = OutputField(
            "Submitted word", font, element_height, parent=self
        )
        response_widget.addWidget(self.__submitted_word)

        self.__translated_word = OutputField(
            "Translated word", font, element_height, parent=self
        )
        response_widget.addWidget(self.__translated_word)

        self.__never_reask_button = PushButton(
            "I learned this word. Don't ask again", font, element_height, parent=self
        )
        self.__never_reask_button.clicked.connect(self.__never_reask)
        response_widget.addWidget(self.__never_reask_button)

        self.__submit_button = PushButton("Submit", font, element_height, parent=self)
        self.__submit_button.clicked.connect(self.__submit_input)
        test_widget.addWidget(self.__submit_button)

        self.__reset_button = PushButton(
            "Reset to default", font, element_height, parent=self
        )
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
            self.__submitted_word.value.setStyleSheet("background-color: lime")
        else:
            self.__submitted_word.value.setStyleSheet("background-color: tomato")

    def set_words_number(self, number: int) -> None:
        self.__words_number.setText(str(number))

    def __submit_input(self) -> None:
        input_text = self.__input_field.text()
        words_number = int(self.__words_number.text())
        self.__submitted_word.setText(input_text)
        self.submitButtonClicked.emit(input_text, words_number)
        self.__input_field.input_field.clear()

    def __never_reask(self) -> None:
        self.neverReaskButtonClicked.emit()
        self.__input_field.input_field.clear()

    def __reset_button_clicked(self) -> None:
        self.resetButtonClicked.emit()
