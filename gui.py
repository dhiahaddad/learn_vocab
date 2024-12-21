from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
)


class MainWindow(QWidget):
    resetButtonClicked = pyqtSignal()
    submitButtonClicked = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Vocabulary Learner")

        self.__layout = QVBoxLayout()

        self.__original_word = QLineEdit(self)
        self.__original_word.setPlaceholderText("Original word")
        self.__original_word.setReadOnly(True)
        self.__layout.addWidget(self.__original_word)

        self.__input_field = QLineEdit(self)
        self.__input_field.setPlaceholderText("Enter your text here")
        self.__input_field.returnPressed.connect(self.__submit_input)
        self.__layout.addWidget(self.__input_field)

        self.__submitted_word = QLineEdit(self)
        self.__submitted_word.setPlaceholderText("Submitted word")
        self.__submitted_word.setReadOnly(True)
        self.__layout.addWidget(self.__submitted_word)

        self.__translated_word = QLineEdit(self)
        self.__translated_word.setPlaceholderText("Translated word")
        self.__translated_word.setReadOnly(True)
        self.__layout.addWidget(self.__translated_word)

        self.__submit_button = QPushButton("Submit", self)
        self.__submit_button.clicked.connect(self.__submit_input)
        self.__layout.addWidget(self.__submit_button)

        self.__reset_button = QPushButton("Reset to default", self)
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
            self.__submitted_word.setStyleSheet("color: green")
        else:
            self.__submitted_word.setStyleSheet("color: red")

    def __submit_input(self) -> None:
        input_text = self.__input_field.text()
        self.__submitted_word.setText(input_text)
        self.submitButtonClicked.emit(input_text)
        self.__input_field.clear()

    def __reset_button_clicked(self) -> None:
        self.resetButtonClicked.emit()
