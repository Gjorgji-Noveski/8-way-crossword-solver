import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap


class CrosswordSolver(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.crosswordPicturePath = None
        self.imageHolder = QLabel(self)
        self.setWindowTitle('PyQt5 App')
        self.setGeometry(100, 100, 280, 80)
        self.move(400, 400)
        self.layout = QVBoxLayout(self)

        chooseCrosswordPicBtn = QPushButton("Choose picture")
        self.layout.addWidget(chooseCrosswordPicBtn)
        chooseCrosswordPicBtn.clicked.connect(self.setPictureFileName)

        # now display the pic

        # after displaying run the image preprocessing

        # run the OCR

    def setPictureFileName(self):
        self.crosswordPicturePath = QFileDialog.getOpenFileName()[0]
        self.imageHolder.setPixmap(QPixmap(self.crosswordPicturePath))
        self.layout.addWidget(self.imageHolder)


app = QApplication([])

myCrosswordSolverWidget = CrosswordSolver()
myCrosswordSolverWidget.show()
sys.exit(app.exec_())
