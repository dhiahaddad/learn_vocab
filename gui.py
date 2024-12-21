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

        self.setLayout = QVBoxLayout()

        self.original_word = QLineEdit(self)
        self.original_word.setPlaceholderText("Original word")
        self.original_word.setReadOnly(True)
        self.layout.addWidget(self.original_word)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter your text here")
        self.input_field.returnPressed.connect(self.submit_input)
        self.layout.addWidget(self.input_field)

        self.submitted_word = QLineEdit(self)
        self.submitted_word.setPlaceholderText("Submitted word")
        self.submitted_word.setReadOnly(True)
        self.layout.addWidget(self.submitted_word)

        self.translated_word = QLineEdit(self)
        self.translated_word.setPlaceholderText("Translated word")
        self.translated_word.setReadOnly(True)
        self.layout.addWidget(self.translated_word)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_input)
        self.layout.addWidget(self.submit_button)

        self.reset_button = QPushButton("Reset to default", self)
        self.reset_button.clicked.connect(self.reset_button_clicked)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)

    def set_original_word(self, word: str) -> None:
        self.original_word.setText(word)

    def set_translated_word(self, word: str) -> None:
        self.translated_word.setText(word)

    def set_submitted_word(self, word: str, correct: bool) -> None:
        self.submitted_word.setText(word)
        if correct:
            self.submitted_word.setStyleSheet("color: green")
        else:
            self.submitted_word.setStyleSheet("color: red")

    def submit_input(self) -> None:
        input_text = self.input_field.text()
        self.submitted_word.setText(input_text)
        self.submitButtonClicked.emit(input_text)
        self.input_field.clear()

    def reset_button_clicked(self) -> None:
        self.resetButtonClicked.emit()
