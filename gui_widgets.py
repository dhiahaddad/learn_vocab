from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)


class BorderedWidget(QWidget):
    def __init__(self, height: int, parent: QWidget):
        super().__init__(parent)
        self.setStyleSheet(
            """
            border: 2px solid black;
            border-radius: 2px;
            """
        )
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setStretch(0, 1)
        self._layout.setStretch(1, 1)
        self.setLayout(self._layout)
        self.setFixedHeight(height)


class InputField(BorderedWidget):
    def __init__(
        self,
        label: str,
        font: QFont,
        height: int,
        parent: QWidget,
    ):
        super().__init__(height, parent)

        self.label = QLabel(label, self)
        self.label.setFont(font)
        self.label.setFixedHeight(round(height * 0.25))
        self.label.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self.label)

        self.input_field = QLineEdit(self)
        self.input_field.setFont(font)
        self.input_field.setFixedHeight(round(height * 0.5))
        self.input_field.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self.input_field)

    def text(self) -> str:
        return self.input_field.text()

    def setText(self, text: str) -> None:
        self.input_field.setText(text)


class OutputField(BorderedWidget):
    def __init__(
        self,
        label: str,
        font: QFont,
        height: int,
        parent: QWidget,
    ) -> None:
        super().__init__(height, parent)

        self.label = QLabel(label, self)
        self.label.setFont(font)
        self.label.setFixedHeight(round(height * 0.25))
        self.label.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self.label)

        self.value = QLabel("", self)
        self.value.setFont(font)
        self.value.setFixedHeight(round(height * 0.5))
        self.value.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self.value)

    def setText(self, text: str) -> None:
        self.value.setText(text)


class PushButton(QPushButton):
    def __init__(
        self,
        text: str,
        font: QFont,
        height: int,
        parent: QWidget,
        bg_color: str = "lightgrey",
    ):
        super().__init__(text, parent)
        self.setFont(font)
        self.setStyleSheet(f"background-color: {bg_color}")
        self.setFixedHeight(round(height * 0.5))


class GroupBox(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        testVBoxLayout = QVBoxLayout(self)
        self.setLayout(testVBoxLayout)

    def addWidget(self, widget: QWidget) -> None:
        self.layout().addWidget(widget)


class StatisticsField(QWidget):
    def __init__(
        self,
        label: str,
        font: QFont,
        height: int,
        parent: QWidget,
    ) -> None:
        super().__init__(parent)

        self._layout = QHBoxLayout(self)

        self.label = QLabel(label + ":", self)
        self.label.setFont(font)
        # self.label.setFixedHeight(round(height*0.25))
        # self.label.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self.label)

        self.value = QLabel("", self)
        self.value.setFont(font)
        # self.value.setFixedHeight(round(height*0.5))
        # self.value.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self.value)

    def setText(self, text: str) -> None:
        self.value.setText(text)


class Statistics(QWidget):
    def __init__(self, font: QFont, height: int, parent: QWidget):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)

        self._words_in_db = StatisticsField("Words in the db", font, height, self)
        self._layout.addWidget(self._words_in_db)

        self._studied_words = StatisticsField("Studied words", font, height, self)
        self._layout.addWidget(self._studied_words)

        self._current_word_lvl = StatisticsField("Current word's learning lvl", font, height, self)
        self._layout.addWidget(self._current_word_lvl)

        self._lvl_1_words = StatisticsField("Words in learning lvl 1", font, height, self)
        self._layout.addWidget(self._lvl_1_words)

        self._lvl_2_words = StatisticsField("Words in learning lvl 2", font, height, self)
        self._layout.addWidget(self._lvl_2_words)

        self._lvl_3_words = StatisticsField("Words in learning lvl 3", font, height, self)
        self._layout.addWidget(self._lvl_3_words)

        self._lvl_4_words = StatisticsField("Words in learning lvl 4", font, height, self)
        self._layout.addWidget(self._lvl_4_words)

        self._lvl_5_words = StatisticsField("Words in learning lvl 5", font, height, self)
        self._layout.addWidget(self._lvl_5_words)

    def set_words_in_db(self, words_in_db: int) -> None:
        self._words_in_db.setText(str(words_in_db))

    def set_studied_words(self, studied_words: int) -> None:
        self._studied_words.setText(str(studied_words))

    def set_current_word_lvl(self, current_word_lvl: int) -> None:        
        self._current_word_lvl.setText(str(current_word_lvl))
    
    def set_words_in_lvl(self, words_in_lvl: list) -> None:
        self._lvl_1_words.setText(str(words_in_lvl[0]))
        self._lvl_2_words.setText(str(words_in_lvl[1]))
        self._lvl_3_words.setText(str(words_in_lvl[2]))
        self._lvl_4_words.setText(str(words_in_lvl[3]))
        self._lvl_5_words.setText(str(words_in_lvl[4]))