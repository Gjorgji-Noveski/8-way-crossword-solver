from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPlainTextEdit


# Disabling "ENTER" key press on search words field to avoid sanitizing input
class PlainTextEdit(QPlainTextEdit):
    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            return
        super().keyPressEvent(event)
