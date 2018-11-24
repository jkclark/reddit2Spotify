from PyQt5.QtWidgets import QLabel as label
from PyQt5.QtCore import pyqtSignal


class CustomConsole(label):
    text_changed = pyqtSignal()

    def __init__(self, initial_message):
        super().__init__()
        self.setText("Console: " + str(initial_message))

    def change_text(self, new_text, error=0):
        self.setText(new_text)
        self.setStyleSheet("color: red") if error else self.setStyleSheet("color: black")
        self.text_changed.emit()
