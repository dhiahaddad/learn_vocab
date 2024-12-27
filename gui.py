import os
import sys
from PyQt5.QtCore import pyqtSlot, QThread
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtWidgets import QApplication
from gui_widgets import GroupBox, PushButton, InputField, OutputField, StatisticsBox
from main import Config, Worker
from progress import Progress

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class MainWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self._create_ui()
        self._start_worker()
        self._update_ui()

    def _update_ui(self):
        new_word = self._worker.load_new_word()
        self._set_words_number(self._worker.words_number)
        self._set_original_word(new_word)
        progress = self._worker.get_progress()
        self._set_progress(progress)
        learned_lvl = self._worker.get_current_learned_lvl()
        self._enable_never_reask_button(learned_lvl)

    def _create_ui(self) -> None:

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

        self._original_word = OutputField(
            "Original word", label_font, element_height, parent=self
        )
        test_widget.addWidget(self._original_word)

        self._input_field = InputField(
            "Enter your text here", label_font, element_height, parent=self
        )
        self._input_field.input_field.returnPressed.connect(self._submit_input)
        test_widget.addWidget(self._input_field)

        self._words_number = InputField(
            "Number of words to be randomized", label_font, element_height, parent=self
        )
        left_layout.addWidget(self._words_number)

        self._submitted_word = OutputField(
            "Submitted word", label_font, element_height, parent=self
        )
        response_widget.addWidget(self._submitted_word)

        self._translated_word = OutputField(
            "Translated word", label_font, element_height, parent=self
        )
        response_widget.addWidget(self._translated_word)

        self._never_reask_button = PushButton(
            "I learned this word. Don't ask again",
            button_font,
            element_height,
            parent=self,
        )
        self._never_reask_button.clicked.connect(self._never_reask)
        response_widget.addWidget(self._never_reask_button)

        self._submit_button = PushButton(
            "Submit", button_font, element_height, parent=self
        )
        self._submit_button.clicked.connect(self._submit_input)
        test_widget.addWidget(self._submit_button)

        reset_layout = QHBoxLayout()
        left_layout.addLayout(reset_layout)

        self._reset_dict_button = PushButton(
            "Reload dictionary", button_font, element_height, parent=self
        )
        self._reset_dict_button.clicked.connect(self._reset_dict_button_clicked)
        reset_layout.addWidget(self._reset_dict_button)

        self._reset_progress_button = PushButton(
            "Reset progress", button_font, element_height, parent=self
        )
        self._reset_progress_button.clicked.connect(self._reset_progress_button_clicked)
        reset_layout.addWidget(self._reset_progress_button)

        self._statistics = StatisticsBox(label_font, element_height, self)
        right_layout.addWidget(self._statistics)

        self.setLayout(main_layout)

    def _start_worker(self) -> None:
        config = Config(
            spreadsheet_url="https://docs.google.com/spreadsheets/d/e/2PACX-1vRW9I6TdJPrc-ow1rdZO_p3_ApEK-W47aA9IwIipDNxFITxX4KaJUx5KG79MIK-XxkDHoIQNuOt5ybq/pub?gid=0&single=true&output=csv",
            test_url="https://docs.google.com/spreadsheets/d/e/2PACX-1vTNAXHYCvnJYyVCNdPCF5JQRclv-RzW3oNvYhrHn6_QdgtIGOV3-AvNPeyWSJn7d4jAWNGWDfsUwY9t/pub?gid=0&single=true&output=csv",
            test_path="test.csv",
            table_name="de_en_vocabulary",
            db_name="learn_language.db",
        )
        self.worker_thread = QThread()
        self._worker = Worker(config)
        self._worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        self._worker.reset_to_default_finished.connect(self._reset_dict_finished)

    def _set_original_word(self, word: str) -> None:
        self._original_word.setText(word)

    def _set_translated_word(self, word: str) -> None:
        self._translated_word.setText(word)

    def _set_submitted_word(self, word: str, correct: bool) -> None:
        self._submitted_word.setText(word)
        if correct:
            self._submitted_word.value.setStyleSheet("background-color: lime")
        else:
            self._submitted_word.value.setStyleSheet("background-color: tomato")

    def _set_words_number(self, number: int) -> None:
        self._words_number.setText(str(number))

    def _set_progress(
        self,
        progress: Progress,
    ) -> None:
        self._statistics.set_words_in_db(progress.words_in_db)
        self._statistics.set_studied_words(progress.studied_words)
        self._statistics.set_current_word_lvl(progress.current_word_lvl)
        self._statistics.set_words_in_lvl(progress.words_in_lvl)

    @pyqtSlot()
    def _submit_input(self) -> None:
        input_text = self._input_field.text()
        words_number = int(self._words_number.text())

        self._worker.set_words_number(words_number)

        result = self._worker.check_answer(input_text)
        self._worker.update_progress_in_db(result)
        self._set_submitted_word(input_text, result)

        translated_word = self._worker.get_translated_word()
        self._set_translated_word(translated_word)

        new_word = self._worker.load_new_word()
        self._set_original_word(new_word)

        learned_lvl = self._worker.get_current_learned_lvl()
        self._enable_never_reask_button(learned_lvl)

        progress = self._worker.get_progress()
        self._set_progress(progress)

        self._input_field.input_field.clear()
        self._input_field.input_field.setFocus()

    @pyqtSlot()
    def _never_reask(self) -> None:

        input_text = self._input_field.text()
        result = self._worker.check_answer(input_text)

        if result:
            self._worker.never_reask()

        self._submit_input()

    @pyqtSlot()
    def _reset_dict_button_clicked(self) -> None:
        self._enable_buttons(False)
        self._worker.reset_to_default_started.emit()

    @pyqtSlot()
    def _reset_dict_finished(self) -> None:
        self._enable_buttons(True)
        self._update_ui()
        self._input_field.input_field.setFocus()

    @pyqtSlot()
    def _reset_progress_button_clicked(self) -> None:
        self._worker.reset_progress()
        progress = self._worker.get_progress()
        self._set_progress(progress)
        self._input_field.input_field.setFocus()

    def _enable_buttons(self, enable: bool = True) -> None:
        self._submit_button.setEnabled(enable)
        self._never_reask_button.setEnabled(enable)
        self._reset_dict_button.setEnabled(enable)
        self._reset_progress_button.setEnabled(enable)
        self._input_field.input_field.setEnabled(enable)
        self._words_number.input_field.setEnabled(enable)

    def _enable_never_reask_button(self, learned_lvl: int) -> None:
        self._never_reask_button.setEnabled(learned_lvl > -1)

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
try:
    sys.exit(app.exec_())
finally:
    main_window._worker.cleanup()
