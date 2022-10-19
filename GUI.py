import subprocess
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import *

from imagePreprocessing import ImgPreprocessing
from overridenFunctionalities import PlainTextEdit, ImageHolder
from textPreprocessing import TextPreprocessing


class CrosswordSolver(QWidget):

    def __init__(self, screen, parent=None):
        super().__init__(parent)
        self.languageSelectedIdx = None
        self.txtPreprocess = TextPreprocessing("tesseract_text.txt")
        self.crosswordPicturePath = None
        self.processedImagePath = 'processed_image.jpg'
        self.resizedImagePath = 'resized_image.jpg'

        self.imageHolder = ImageHolder(self)
        self.setWindowTitle('PyQt5 App')
        self.setGeometry(100, 100, 280, 80)
        self.move(400, 400)
        self.layout = QVBoxLayout(self)
        self.scrollArea = None

        # Layouts
        frame1 = QFrame(self)
        frame1.setFrameShape(QFrame.Box)
        # frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        frame1.setLineWidth(3)

        frame2 = QFrame(self)
        frame2.setFrameShape(QFrame.Box)
        # frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        frame2.setLineWidth(3)

        # frame2 = QFrame(self)
        # frame2.setFrameShape(QFrame.Box)
        # # frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        # frame2.setLineWidth(3)

        self.subLayout1h = QHBoxLayout(self)
        self.subLayout1hChild1 = QVBoxLayout(frame1)
        self.subLayout1hChild2 = QVBoxLayout(frame2)

        self.subLayout1hChild1.setAlignment(Qt.AlignLeft)
        self.subLayout1hChild2.setAlignment(Qt.AlignLeft)

        self.subLayout1h.addWidget(frame1)
        self.subLayout1h.addWidget(frame2)
        # self.subLayout1h.setStretch(1, 1)  # This fixes the layout in place, so the widgets don't move



        self.subLayout2h = QHBoxLayout(self)
        self.subLayout3h = QHBoxLayout(self)
        self.subLayout4h = QHBoxLayout(self)


        self.layout.addLayout(self.subLayout1h)
        self.layout.addLayout(self.subLayout2h)
        self.layout.addLayout(self.subLayout3h)
        self.layout.addLayout(self.subLayout4h)


        # Language button
        self.languageLabel = QLabel(self)
        self.languageLabel.setText("What is the language of the letters in the word grid?")
        self.subLayout1hChild1.addWidget(self.languageLabel)
        self.languageSelectBox = QComboBox(self)
        self.languageSelectBox.setFixedWidth(int(screen.availableSize().width() * 0.08))  # 10$ of the screen's width
        self.languageSelectBox.addItem("Macedonian (MK)", "mkd")
        self.languageSelectBox.addItem("English (EN)", "eng")
        self.languageSelectBox.currentIndexChanged.connect(self.rerunOcr)
        self.subLayout1hChild1.addWidget(self.languageSelectBox)

        self.subLayout2h.addWidget(self.imageHolder)

        chooseCrosswordPicBtn = QPushButton("Choose picture")
        self.subLayout3h.addWidget(chooseCrosswordPicBtn)
        chooseCrosswordPicBtn.clicked.connect(self.dialogSelectImage)

        # Input text widget
        self.textBox = PlainTextEdit(self)
        self.textBox.setPlaceholderText("Insert search words separated by space, ex: tree cat sky")
        self.textBox.setMaximumHeight(200)
        self.subLayout2h.addWidget(self.textBox)

        # Search Words button
        self.searchWordsBtn = QPushButton("Search words")
        self.searchWordsBtn.setDisabled(True)
        self.subLayout3h.addWidget(self.searchWordsBtn)
        self.searchWordsBtn.clicked.connect(self.searchForWords)

        # Columns in word word field
        self.columnLabel = QLabel(self)
        self.columnLabel.setText("How many columns does the word grid have?")
        self.subLayout1hChild2.addWidget(self.columnLabel)
        self.columnsField = QSpinBox(self)
        self.columnsField.setValue(10)
        self.columnsField.setMaximumWidth(int(screen.availableSize().width() * 0.04))
        self.subLayout1hChild2.addWidget(self.columnsField)

        # Displaying results
        self.resultLabel = QLabel(self)
        self.resultLabel.setFont(QFont("Arial", 15))
        self.resultLabel.setWordWrap(True)
        self.resultLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.resultsLabelInfoText = QLabel(self)
        self.resultsLabelInfoText.setText("Results from search are:")
        self.subLayout4h.addWidget(self.resultsLabelInfoText)
        # self.layout.addWidget(self.resultLabel)
        self.resultLabel.setMinimumHeight(int(screen.availableSize().height() * 0.1))

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.resultLabel)
        self.layout.addWidget(self.scrollArea)

    def rerunOcr(self):
        if self.crosswordPicturePath:
            self.runOCR()

    def searchForWords(self):
        words = set()
        for element in self.textBox.toPlainText().split(' '):
            words.add(element)
        result = ""
        for word in words:
            if word.strip() == '':
                continue
            foundWord = self.txtPreprocess.search(word)
            if foundWord:
                result += foundWord
        if result == "":
            result += "No matches found"
        self.resultLabel.setText(result)

    def runImgPreprocessing(self, picture_path):
        ImgPreprocessing.preproces_image(picture_path, self.columnsField.value())

    def dialogSelectImage(self):
        selectedImgPath = QFileDialog.getOpenFileName()[0]
        if selectedImgPath:
            self.crosswordPicturePath = selectedImgPath
            self.runImgPreprocessing(self.crosswordPicturePath)
            self.imageHolder.setPixmap(QPixmap(self.resizedImagePath))
            self.runOCR()
            self.searchWordsBtn.setDisabled(False)

    def runOCR(self):
        subprocess_result = subprocess.run(
            ['tesseract', self.processedImagePath, 'tesseract_text', '-l', self.languageSelectBox.currentData(),
             '-psm', '6'], capture_output=True,
            text=True, encoding="UTF-8")
        print(f'Tesseract Stdout: {subprocess_result.stdout}')
        print(f'Tesseract Stderr: {subprocess_result.stderr}')


app = QApplication([])

myCrosswordSolverWidget = CrosswordSolver(app.primaryScreen(), parent=app.parent())
myCrosswordSolverWidget.show()
sys.exit(app.exec_())
