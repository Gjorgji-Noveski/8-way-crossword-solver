import subprocess
import sys
import platform

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import *

from imageProcessing import ImgProcessing
from overridenFunctionalities import PlainTextEdit, ImageHolder
from textProcessing import TextProcessing


class CrosswordSolver(QWidget):

    def __init__(self, screen, parent=None):
        super().__init__(parent)
        self.screen = screen
        self.languageSelectedIdx = None
        self.txtProcess = TextProcessing("tesseract_text.txt")
        self.crosswordPicturePath = None
        self.processedImagePath = 'processed_image.jpg'
        self.displayedImgPath = 'displayed_image.jpg'
        self.resizedImagePath = 'resized_image.jpg'

        self.setWindowTitle('8-way crossword solver')
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

        frame3 = QFrame(self)
        frame3.setFrameShape(QFrame.Box)
        frame3.setMaximumWidth(int(screen.availableSize().width() * 0.5))
        frame3.setLineWidth(3)

        self.subLayout1h = QHBoxLayout(self)
        self.subLayout1hChild1 = QVBoxLayout(frame1)
        self.subLayout1hChild2 = QVBoxLayout(frame2)

        self.subLayout1hChild1.setAlignment(Qt.AlignLeft)
        self.subLayout1hChild2.setAlignment(Qt.AlignLeft)

        self.subLayout1h.addWidget(frame1)
        self.subLayout1h.addWidget(frame2)
        # self.subLayout1h.setStretch(1, 1)  # This fixes the layout in place, so the widgets don't move

        self.subLayout2h = QHBoxLayout(self)
        self.subLayout2hChild = QVBoxLayout(frame3)
        self.subLayout2hChild.setAlignment(Qt.AlignLeft)
        self.subLayout3h = QHBoxLayout(self)

        self.layout.addLayout(self.subLayout1h)
        self.layout.addLayout(self.subLayout2h)
        self.layout.addLayout(self.subLayout3h)

        # Language button
        self.languageLabel = QLabel(frame1)
        self.languageLabel.setText("What is the language of the letters in the word grid?")
        self.subLayout1hChild1.addWidget(self.languageLabel)
        self.languageSelectBox = QComboBox(frame1)
        self.languageSelectBox.setFixedWidth(int(screen.availableSize().width() * 0.08))  # 10$ of the screen's width
        self.languageSelectBox.addItem("Macedonian (MK)", "mkd")
        self.languageSelectBox.addItem("English (EN)", "eng")
        self.languageSelectBox.currentIndexChanged.connect(self.rerunOcr)
        self.subLayout1hChild1.addWidget(self.languageSelectBox)

        self.imageHolder = ImageHolder(self)
        self.imageHolder.setDisabled(True)

        self.subLayout2h.addWidget(self.imageHolder)
        self.subLayout2h.addWidget(frame3)

        chooseCrosswordPicBtn = QPushButton("Choose picture")
        chooseCrosswordPicBtn.setMinimumHeight(int(screen.availableSize().height() * 0.05))
        self.subLayout3h.addWidget(chooseCrosswordPicBtn)
        chooseCrosswordPicBtn.clicked.connect(self.dialogSelectImage)

        # Input text widget
        self.textBox = PlainTextEdit(frame3)

        self.textBox.setPlaceholderText("Insert search words separated by space, ex: tree cat sky")
        self.textBox.setMaximumHeight(int(screen.availableSize().height() * 0.12))
        self.subLayout2hChild.addWidget(self.textBox)

        # Search Words button
        self.searchWordsBtn = QPushButton("Search words")
        self.searchWordsBtn.setMinimumHeight(
            int(screen.availableSize().height() * 0.05))  # the buttons should be at least 5% of the screens available size
        self.searchWordsBtn.setDisabled(True)
        self.subLayout3h.addWidget(self.searchWordsBtn)
        self.searchWordsBtn.clicked.connect(self.searchForWords)

        # Columns in word word field
        self.columnLabel = QLabel(frame2)
        self.columnLabel.setText("How many columns does the word grid have?")
        self.subLayout1hChild2.addWidget(self.columnLabel)
        self.columnsField = QSpinBox(frame2)
        self.columnsField.setValue(10)
        self.columnsField.setMinimum(1)
        self.columnsField.setMaximumWidth(int(screen.availableSize().width() * 0.04))
        self.subLayout1hChild2.addWidget(self.columnsField)

        def call_img_process_and_ocr():
            if self.crosswordPicturePath:
                self.runImgProcessing(self.displayedImgPath)
                self.runOCR()
        self.columnsField.valueChanged.connect(call_img_process_and_ocr)

        # Displaying results
        self.resultLabel = QLabel(frame3)
        self.resultLabel.setFont(QFont("Arial", 15))
        self.resultLabel.setWordWrap(True)
        self.resultLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.resultsLabelInfoText = QLabel(frame3)
        self.resultsLabelInfoText.setText("Results from search are:")
        self.subLayout2hChild.addWidget(self.resultsLabelInfoText)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.resultLabel)

        self.subLayout2hChild.addWidget(self.scrollArea)

    def rerunOcr(self):
        if self.crosswordPicturePath:
            self.runOCR()

    def searchForWords(self):
        words = set()
        result = ""

        for element in self.textBox.toPlainText().split(' '):
            if len(element) > 1:
                words.add(element)
            else:
                result += "---Single letter found, skipping---\n\n"
        for word in words:
            if word.strip() == '':
                continue
            foundWord = self.txtProcess.search(word)
            if foundWord:
                result += foundWord
        if result == "":
            result += "No matches found"
        self.resultLabel.setText(result)

    def runImgProcessing(self, picture_path):
        if self.crosswordPicturePath:
            ImgProcessing.process_image(picture_path, self.columnsField.value())

    def runImgResizing(self, picture_path):
        if self.crosswordPicturePath:
            maxHeightOfResizedImage = int(self.screen.availableSize().height() * 0.8)
            ImgProcessing.save_resized_img(picture_path, self.columnsField.value(), maxHeightOfResizedImage)

    def dialogSelectImage(self):
        selectedImgPath = QFileDialog.getOpenFileName()[0]
        if selectedImgPath:
            self.crosswordPicturePath = selectedImgPath
            self.runImgResizing(self.crosswordPicturePath)
            self.runImgProcessing(self.crosswordPicturePath)
            self.imageHolder.setDisabled(False)
            self.imageHolder.setPixmap(QPixmap(self.resizedImagePath))
            ImgProcessing.save_img('displayed_image.jpg', self.crosswordPicturePath)
            self.imageHolder.setFixedSize(self.imageHolder.pixmap().rect().width(),
                                          self.imageHolder.pixmap().rect().height())

            self.runOCR()
            self.searchWordsBtn.setDisabled(False)

    def runOCR(self):
        if platform.system().lower() == "windows":

            subprocess_result = subprocess.run(
                ['tesseract.exe', self.processedImagePath, 'tesseract_text', '-l', self.languageSelectBox.currentData(),
                 '--psm', '6'], capture_output=True,
                text=True, encoding="UTF-8")
        else:
            subprocess_result = subprocess.run(
                ['tesseract', self.processedImagePath, 'tesseract_text', '-l', self.languageSelectBox.currentData(),
                 '--psm', '6'], capture_output=True,
                text=True, encoding="UTF-8")
        # print(f'Tesseract Stdout: {subprocess_result.stdout}')
        # print(f'Tesseract Stderr: {subprocess_result.stderr}')


app = QApplication([])

myCrosswordSolverWidget = CrosswordSolver(app.primaryScreen(), parent=app.parent())
myCrosswordSolverWidget.showMaximized()
myCrosswordSolverWidget.show()
sys.exit(app.exec_())
