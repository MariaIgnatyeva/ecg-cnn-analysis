# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'appui.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5.QtCore import Qt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

import app_logic
import wfdb
from wfdb import processing
from model import ECGModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QProgressDialog, QSizePolicy, QScrollArea, QDesktopWidget, QMainWindow, \
    QVBoxLayout, QLabel, QHBoxLayout, QWidget, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=15, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.initMembers()

        super().__init__(self.fig)
        self.setParent(parent)
        self.grid(True)
        self.fig.set_tight_layout(True)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Fixed)

    def initMembers(self):
        pass

    def grid(self, show):
        self.axes.grid(show)
        self.draw()


class Window(QMainWindow):
    plotCanvas = None

    def __init__(self):
        super().__init__()
        self.title = 'Heart Atthythmia Classification Using Neural Network'
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
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar()
        helpMenu = mainMenu.addMenu('&Help')
        # helpMenu.addAction(helpAction)
        # helpMenu.addAction(aboutAction)

        self.fileChooseButton = QtWidgets.QPushButton('Choose file')
        self.fileChooseButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.fileChooseButton.clicked.connect(self.showFilesDialog)

        self.classifyButton = QtWidgets.QPushButton('Classify')
        self.classifyButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.classifyButton.clicked.connect(self.plotResuts)

        self.predButtonsVLayout = QVBoxLayout()
        self.predButtonsVLayout.addWidget(self.fileChooseButton)
        self.predButtonsVLayout.addWidget(self.classifyButton)

        self.uploadFileLabel = QLabel('Upload data file:')
        self.uploadFileLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.uploadFileLabel.setAlignment(Qt.AlignTop)
        self.uploadFileLabel.setMargin(7)

        self.chosenFileName = QLabel('No file chosen')
        self.chosenFileName.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.chosenFileName.setAlignment(Qt.AlignTop)
        self.chosenFileName.setMargin(7)

        self.predHLayout = QHBoxLayout()
        self.predHLayout.setSpacing(15)
        self.predHLayout.setAlignment(Qt.AlignTop)
        self.predHLayout.addWidget(self.uploadFileLabel)
        self.predHLayout.addLayout(self.predButtonsVLayout)
        self.predHLayout.addWidget(self.chosenFileName)

        self.scrollArea = QScrollArea()
        self.scrollArea.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.scrollArea.setFixedHeight(300)
        self.scrollArea.setAlignment(Qt.AlignTop)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.predHLayout)
        self.mainLayout.addWidget(self.scrollArea)

        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        self.show()

    def showFilesDialog(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Choose file')[0]  # , filter="Text files (*.txt *.csv)")
        self.chosenFileName.setText(self.fname[self.fname.rfind('/') + 1:] if self.fname != '' else 'No file chosen')
        self.classifyButton.setEnabled(self.fname != '')

    def readData(self):
        signals = []
        fs = 0
        with open(self.fname, 'r') as fin:
            fs = int(fin.readline())
            for line in fin.readlines():
                signals.append(float(line))
        signals = np.array(signals)

        return fs, signals

    def getQRSInds(self, signals, fs):
        xqrs = processing.XQRS(sig=np.array(signals), fs=fs)
        xqrs.detect()

        return xqrs.qrs_inds

    def getPredictions(self, signals, fs):
        model = ECGModel('model')
        return model.predict(signals, fs)

    def plotResuts(self):
        fs, signals = self.readData()
        qrs_inds = self.getQRSInds(signals, fs)
        # pred_classes = self.getPredictions(signals, fs)
        pred_classes = ['nor', 'nor', 'apc', 'nor']

        self.plotCanvas = PlotCanvas(width=len(signals) // 120)
        self.plotCanvas.axes.xaxis.set_major_locator(MultipleLocator(50))
        self.plotCanvas.axes.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        self.plotCanvas.axes.xaxis.set_minor_locator(MultipleLocator(10))
        self.plotCanvas.axes.yaxis.set_major_locator(MultipleLocator(0.5))
        self.plotCanvas.axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        self.plotCanvas.axes.yaxis.set_minor_locator(MultipleLocator(0.1))
        self.plotCanvas.axes.set_ylim(min(signals) - 0.1, max(signals) + 0.3)
        self.plotCanvas.axes.set_xlim(0, len(signals))
        self.plotCanvas.axes.grid(True, which='major', linewidth=1, color='r', alpha=0.15)
        self.plotCanvas.axes.grid(True, which='minor', linewidth=0.5, color='r', alpha=0.15)

        self.plotCanvas.axes.plot(signals, color='k')
        self.plotCanvas.fig.set_tight_layout(True)

        for i, ind in enumerate(qrs_inds[:len(pred_classes)]):
            color = 'b' if pred_classes[i] == 'nor' else 'r'
            self.plotCanvas.axes.annotate(pred_classes[i].upper(), (ind - 15, 1), color=color, fontsize=14)

        self.plotCanvas.draw()

        self.scrollArea.setWidget(self.plotCanvas)
        self.scrollArea.setMinimumHeight(
            self.scrollArea.widget().sizeHint().height() + self.scrollArea.horizontalScrollBar().sizeHint().height() + 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
