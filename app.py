from PyQt5.QtGui import QIcon

import sys
import numexpr as ne
import numpy as np
import matplotlib.patches as patches
import matplotlib.lines as lines

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QPushButton, QComboBox, QStackedLayout, QCheckBox,
                             QSizePolicy, QLineEdit, QHBoxLayout, QVBoxLayout, QGroupBox, QWidget, QLabel,
                             QFormLayout, QScrollArea, QListWidget, QDoubleSpinBox, QMessageBox, QDesktopWidget,
                             QProgressDialog, QRadioButton, QMainWindow, QAction, QDialog, QTextEdit, QToolButton,
                             QFileDialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.figure import Figure

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Heart Arrhythmia Classification Using Neural Network'
        self.setSize()
        self.initUI()

    def setSize(self):
        desktop = QDesktopWidget()
        size = desktop.screenGeometry()

        self.left = size.width() // 9
        self.top = size.height() // 20
        self.width = size.width() - self.left * 2
        self.height = size.height() - self.top * 2 - 100

    def initUI(self):
        fileChooseLayout = QHBoxLayout()

        fileUploadLabel = QLabel('Upload data file:')
        fileUploadLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        fileChooseLayout.addWidget(fileUploadLabel)

        fileChooseButton = QPushButton('Choose file')
        fileChooseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        fileChooseButton.clicked.connect(self.showDialog)
        fileChooseLayout.addWidget(fileChooseButton)
        fileChooseLayout.setAlignment(fileChooseButton, Qt.AlignLeft)

        self.chosenFileName = QLabel('No file chosen')
        self.chosenFileName.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        fileChooseLayout.addWidget(self.chosenFileName)
        fileChooseLayout.setAlignment(self.chosenFileName, Qt.AlignLeft)

        fileUploadLayout = QVBoxLayout()
        fileUploadLayout.addLayout(fileChooseLayout)

        uploadButton = QPushButton('Upload')
        uploadButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.textEdit = QTextEdit()
        uploadButton.clicked.connect(self.setText)

        fileUploadLayout.addWidget(uploadButton)
        fileUploadLayout.addWidget(self.textEdit)
        centralWidget = QWidget()
        centralWidget.setLayout(fileUploadLayout)

        self.setCentralWidget(centralWidget)
        # self.setLayout(fileChooseLayout)

        # self.textEdit = QTextEdit()
        # self.setCentralWidget(self.textEdit)
        # self.statusBar()

        # openFile = QAction(QIcon('open.png'), 'Open', self)
        # openFile.setShortcut('Ctrl+O')
        # openFile.setStatusTip('Open new File')
        # openFile.triggered.connect(self.showDialog)
        #
        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(openFile)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

    def showDialog(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Choose file')[0] #, filter="Text files (*.txt *.csv)")
        self.chosenFileName.setText(self.fname[self.fname.rfind('/') + 1:])

    def setText(self):
        f = open(self.fname, 'r')
        with f:
            self.data = f.read()

        self.textEdit.setText(self.data)

    # def showHelp(self):
    #     help = Help()
    #     help.exec()
    #
    # def showAbout(self):
    #     about = About()
    #     about.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())