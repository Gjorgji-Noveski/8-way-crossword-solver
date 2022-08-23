import sys, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, QSize
from imagePreprocessing import ImgPreprocessing
from textPreprocessing import TextPreprocessing
from PyQt5.QtGui import QIntValidator

class CrosswordSolver(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cropArea = None
        self.initialClickPos = None
        self.resultText = ""
        self.txtPreprocess = TextPreprocessing("tesseract_text.txt")
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

        # Columns in word word field
        self.columnLabel = QLabel(self)
        self.columnLabel.setText("How many columns does the word grid have?")
        self.layout.addWidget(self.columnLabel)
        self.columnsField = QSpinBox(self)
        self.columnsField.setValue(10)
        self.columnsField.setMaximumWidth(100)
        self.layout.addWidget(self.columnsField)

        # Displaying results
        self.resultLabel = QLabel(self)
        self.layout.addWidget(self.resultLabel)

    def searchForWords(self):
        words = self.textBox.toPlainText().split(' ')
        result = ""
        for word in words:
            foundWord = self.txtPreprocess.search(word)
            if foundWord:
                result += foundWord
        self.resultText = result
        self.resultLabel.setText(self.resultText)


    def processImage(self):
        selectedImgPath = QFileDialog.getOpenFileName()[0]
        if selectedImgPath:
            self.crosswordPicturePath = selectedImgPath
            ImgPreprocessing.preproces_image(self.crosswordPicturePath, self.columnsField.value())
            self.imageHolder.setPixmap(QPixmap("resized_img.jpg"))

            print(f"'{self.crosswordPicturePath}'")
            subprocess_result = subprocess.run(
                ['tesseract', self.processedImagePath, 'tesseract_text', '-l', 'mkd', '-psm', '6'], capture_output=True,
                text=True, encoding="UTF-8")
            print(f'Tesseract Stdout: {subprocess_result.stdout}')
            print(f'Tesseract Stderr: {subprocess_result.stderr}')

            self.searchWordsBtn.setDisabled(False)

    def mousePressEvent(self, event):
        origin = event.pos()
        self.initialClickPos = origin
        self.cropArea = QRubberBand(QRubberBand.Rectangle, self)
        self.cropArea.setGeometry(QRect(origin, QSize()))
        self.cropArea.show()

    def mouseMoveEvent(self, event):
        self.cropArea.setGeometry(QRect(self.initialClickPos, event.pos()).normalized())

    # def mouseReleaseEvent(self, event):
    #     self.rubberBand.hide()
    #     # determine selection, for example using QRect.intersects()
    #     # and QRect.contains().

app = QApplication([])

myCrosswordSolverWidget = CrosswordSolver()
myCrosswordSolverWidget.show()
sys.exit(app.exec_())
