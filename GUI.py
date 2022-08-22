import sys, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from imagePreprocessing import preproces_image
from textPreprocessing import TextPreprocessing

class CrosswordSolver(QWidget):



    def __init__(self, parent=None):
        self.txtPreprocess = TextPreprocessing("tesseract_text11.txt")
        super().__init__(parent)
        self.crosswordPicturePath = None
        self.processedImagePath = 'processed_image.jpg'
        self.imageHolder = QLabel(self)
        self.setWindowTitle('PyQt5 App')
        self.setGeometry(100, 100, 280, 80)
        self.move(400, 400)
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.imageHolder)

        chooseCrosswordPicBtn = QPushButton("Choose picture")
        self.layout.addWidget(chooseCrosswordPicBtn)
        chooseCrosswordPicBtn.clicked.connect(self.processImage)

        # Input text widget
        self.textBox = QPlainTextEdit(self)
        self.textBox.setPlaceholderText("Insert search words separated by space, ex: tree cat sky")
        self.layout.addWidget(self.textBox)

        # Search Words button
        self.searchWordsBtn = QPushButton("Search words")
        self.searchWordsBtn.setDisabled(True)
        self.layout.addWidget(self.searchWordsBtn)
        self.searchWordsBtn.clicked.connect(self.searchForWords)

        # read generated txt file

        # Process to find words againts txt file (review your code if it works
        # )
    def searchForWords(self):
        words = self.textBox.toPlainText().split(' ')
        for word in words:
            self.txtPreprocess.search(word)

    def processImage(self):
        self.crosswordPicturePath = QFileDialog.getOpenFileName()[0]
        self.imageHolder.setPixmap(QPixmap(self.crosswordPicturePath))
        preproces_image(self.crosswordPicturePath)
        print(f"'{self.crosswordPicturePath}'")
        subprocess_result = subprocess.run(
            ['tesseract', self.processedImagePath, 'tesseract_text', '-l', 'mkd', '-psm', '11'], capture_output=True,
            text=True, encoding="UTF-8")
        print(f'Tesseract Stdout: {subprocess_result.stdout}')
        print(f'Tesseract Stderr: {subprocess_result.stderr}')

        self.searchWordsBtn.setDisabled(False)


app = QApplication([])

myCrosswordSolverWidget = CrosswordSolver()
myCrosswordSolverWidget.show()
sys.exit(app.exec_())
