from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QPlainTextEdit, QLabel, QRubberBand


# Disabling "ENTER" key press on search words field to avoid sanitizing input
class PlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            return
        super().keyPressEvent(event)

#TODO: problem: start program, open tall image krstozbor(1).jpg, reside window of widget for fullscreen, crop, and you will see it doesnt get cropped correctly
# This happens only for the tall pic, for the krsozbor clean.jpg it doesnt happen

"""
THIS MAKES problem with the crop after full window resize
self.setpixmap(self.pixmap().copy(Qrect(self.geometry().intersected(self.cropArea.geometry()))))

THIS DOESNT
self.setpixmap(self.pixmap().copy(self.cropArea.geometry())
"""
class ImageHolder(QLabel):

    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(parent)
        self.initialClickPos = None
        self.cropArea = None

    def mousePressEvent(self, event):
        print(f'Mouse clicked: {event.pos()}')
        origin = event.pos()
        self.initialClickPos = origin
        self.cropArea = QRubberBand(QRubberBand.Rectangle, self)
        self.cropArea.setGeometry(QRect(origin, QSize()))
        self.cropArea.show()

    def mouseMoveEvent(self, event):
        self.cropArea.setGeometry(QRect(self.initialClickPos, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.cropArea.hide()
        print(f'cropped area after realese:{self.cropArea.rect()}')
        newImg = self.pixmap().copy(self.cropArea.geometry())
        self.setPixmap(newImg)
        newImg.save(self.parent.crosswordPicturePath)
        self.cropArea.deleteLater()

        self.parent.runImgPreprocessing()
        # print(self.children())