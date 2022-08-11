import sys, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from OCR import preproces_image

class CrosswordSolver(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.crosswordPicturePath = None
        self.processedImagePath = "processed_image"
        self.imageHolder = QLabel(self)
        self.setWindowTitle('PyQt5 App')
        self.setGeometry(100, 100, 280, 80)
        self.move(400, 400)
        self.layout = QVBoxLayout(self)

        chooseCrosswordPicBtn = QPushButton("Choose picture")
        self.layout.addWidget(chooseCrosswordPicBtn)
        chooseCrosswordPicBtn.clicked.connect(self.setPictureFileName)

        preproces_image(self.crosswordPicturePath)

        # run the OCR
        subprocess_result = subprocess.run(
            ['tesseract', self.processedImagePath, 'tesseract_text', '-l', 'mkd', '-psm', '11'], capture_output=True, text=True)
        print(f'Tesseract Stdout: {subprocess_result.stdout}')
        print(f'Tesseract Stderr: {subprocess_result.stderr}')

        # put input text widget to search for all the words

        # read generated txt file

        # Process to find words againts txt file (review your code if it works
        # )
    def setPictureFileName(self):
        self.crosswordPicturePath = QFileDialog.getOpenFileName()[0]
        self.imageHolder.setPixmap(QPixmap(self.crosswordPicturePath))
        self.layout.addWidget(self.imageHolder)


app = QApplication([])

myCrosswordSolverWidget = CrosswordSolver()
myCrosswordSolverWidget.show()
sys.exit(app.exec_())
