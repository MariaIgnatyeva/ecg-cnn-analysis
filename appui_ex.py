# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'appui.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(886, 643)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 10, 891, 451))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.predObjectsHLayout = QtWidgets.QHBoxLayout()
        self.predObjectsHLayout.setContentsMargins(15, 0, 15, -1)
        self.predObjectsHLayout.setSpacing(10)
        self.predObjectsHLayout.setObjectName("predObjectsHLayout")
        self.filUploadLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filUploadLabel.sizePolicy().hasHeightForWidth())
        self.filUploadLabel.setSizePolicy(sizePolicy)
        self.filUploadLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.filUploadLabel.setObjectName("filUploadLabel")
        self.predObjectsHLayout.addWidget(self.filUploadLabel)
        self.predButtonsVLayout = QtWidgets.QVBoxLayout()
        self.predButtonsVLayout.setObjectName("predButtonsVLayout")
        self.fileChooseButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileChooseButton.sizePolicy().hasHeightForWidth())
        self.fileChooseButton.setSizePolicy(sizePolicy)
        self.fileChooseButton.setObjectName("fileChooseButton")
        self.predButtonsVLayout.addWidget(self.fileChooseButton)
        self.fileUploadButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileUploadButton.sizePolicy().hasHeightForWidth())
        self.fileUploadButton.setSizePolicy(sizePolicy)
        self.fileUploadButton.setObjectName("fileUploadButton")
        self.predButtonsVLayout.addWidget(self.fileUploadButton)
        self.predObjectsHLayout.addLayout(self.predButtonsVLayout)
        self.chosenFileName = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chosenFileName.sizePolicy().hasHeightForWidth())
        self.chosenFileName.setSizePolicy(sizePolicy)
        self.chosenFileName.setFocusPolicy(QtCore.Qt.NoFocus)
        self.chosenFileName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.chosenFileName.setObjectName("chosenFileName")
        self.predObjectsHLayout.addWidget(self.chosenFileName)
        self.verticalLayout.addLayout(self.predObjectsHLayout)
        self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 887, 357))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 886, 31))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Heart Atthythmia Classification Using Neural Network"))
        self.filUploadLabel.setText(_translate("MainWindow", "Upload data file:"))
        self.fileChooseButton.setText(_translate("MainWindow", "Choose file"))
        self.fileUploadButton.setText(_translate("MainWindow", "Classify"))
        self.chosenFileName.setText(_translate("MainWindow", "No file chosen"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
