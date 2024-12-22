from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
)


class InOutField(QLineEdit):
    def __init__(
        self,
        placeholder: str,
        font: QFont,
        height: int,
        parent: QWidget,
        readonly: bool = False,
    ):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setReadOnly(readonly)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(font)
        self.setFixedHeight(height)


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
        font.setBold(True)
        font.setFamily("Arial")
        self.setFont(font)
        self.setStyleSheet(f"background-color: {bg_color}")
        self.setFixedHeight(height)
