from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
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
        self.label.setFixedHeight(round(height*0.25))
        self.label.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self.label)

        self.input_field = QLineEdit(self)
        self.input_field.setFont(font)
        self.input_field.setFixedHeight(round(height*0.5))
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
        self.label.setFixedHeight(round(height*0.25))
        self.label.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self.label)

        self.value = QLabel("", self)
        self.value.setFont(font)
        self.value.setFixedHeight(round(height*0.5))
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
        font.setBold(True)
        font.setFamily("Arial")
        self.setFont(font)
        self.setStyleSheet(f"background-color: {bg_color}")
        self.setFixedHeight(round(height * 0.5))


class GroupBox(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        testVBoxLayout = QVBoxLayout()
        self.setLayout(testVBoxLayout)

    def addWidget(self, widget: QWidget) -> None:
        self.layout().addWidget(widget)
