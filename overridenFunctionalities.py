from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtWidgets import QPlainTextEdit, QLabel, QRubberBand


# Disabling "ENTER" key press on search words field to avoid sanitizing input
class PlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            return
        super().keyPressEvent(event)


# TODO: problem: start program, open tall image krstozbor(1).jpg, reside window of widget for fullscreen, crop, and you will see it doesnt get cropped correctly
# This happens only for the tall pic, for the krsozbor clean.jpg it doesnt happen.


"""
THIS MAKES problem with the crop after full window resize
self.setpixmap(self.pixmap().copy(Qrect(self.geometry().intersected(self.cropArea.geometry()))))

THIS DOESNT
self.setpixmap(self.pixmap().copy(self.cropArea.geometry())
"""


class ImageHolder(QLabel):

    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.initialClickPos = None
        self.cropArea = None

    def mousePressEvent(self, event):
        self.initialClickPos = event.pos()
        self.cropArea = QRubberBand(QRubberBand.Rectangle, self)
        self.cropArea.setGeometry(QRect(self.initialClickPos, QSize()))
        self.cropArea.show()

    def mouseMoveEvent(self, event):
        self.cropArea.setGeometry(QRect(self.initialClickPos, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.cropArea.hide()
        newImg = self.pixmap().copy(self.cropArea.geometry())
        self.setPixmap(newImg)
        self.setFixedSize(self.pixmap().rect().width(), self.pixmap().rect().height())
        newImg.save(self.parent.resizedImagePath)
        self.cropArea.deleteLater()

        self.parent.runImgPreprocessing(self.parent.resizedImagePath)
        self.parent.rerunOcr()
