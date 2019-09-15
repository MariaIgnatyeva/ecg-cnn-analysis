import sys

from PyQt5.QtCore import Qt

import os
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QProgressDialog, QSizePolicy, QScrollArea, QDesktopWidget, QMainWindow, \
    QVBoxLayout, QLabel, QHBoxLayout, QWidget, QApplication, QAbstractScrollArea, QAction, QDialog, QPushButton, \
    QMessageBox
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from constants import *
import analysis
from canvas import PlotCanvas


class Appication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.initUI()
        self.analysis = analysis.CNNAnalysis()

    def initUI(self):
        self.init_menu()

        self.upload_file_label = QLabel('Upload data file:')
        self.upload_file_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.upload_file_label.setAlignment(Qt.AlignTop)
        self.upload_file_label.setContentsMargins(0, 7, 0, 0)

        self.choose_data_button = QPushButton('Choose file')
        self.choose_data_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.choose_data_button.clicked.connect(self.show_files_dialog)

        self.data_fname_label = QLabel('No file chosen')
        self.data_fname_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.data_fname_label.setAlignment(Qt.AlignTop)
        self.data_fname_label.setContentsMargins(0, 7, 0, 0)

        self.classify_button = QPushButton('Classify')
        self.classify_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.classify_button.clicked.connect(self.plot_results)

        self.buttons_vlayout = QVBoxLayout()
        self.buttons_vlayout.addWidget(self.choose_data_button)
        self.buttons_vlayout.addWidget(self.classify_button)

        self.pred_hlayout = QHBoxLayout()
        self.pred_hlayout.setAlignment(Qt.AlignTop)
        self.pred_hlayout.addWidget(self.upload_file_label)
        self.pred_hlayout.addLayout(self.buttons_vlayout)
        self.pred_hlayout.addWidget(self.data_fname_label)

        self.canvas = PlotCanvas()
        self.nav_toolbar = NavigationToolbar(self.canvas, self)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.nav_toolbar)

        # TODO: height
        self.scroll_area = QScrollArea()
        self.scroll_area.setAlignment(Qt.AlignTop)
        self.scroll_area.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.scroll_area.setMinimumHeight(
            int(FIG_H * DPI) + self.scroll_area.horizontalScrollBar().sizeHint().height() + 2)
        # self.scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scroll_area.setWidget(self.canvas)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.addLayout(self.pred_hlayout)
        self.main_layout.addWidget(self.scroll_area)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.showMaximized()

    def init_menu(self):
        self.help_action = QAction('&Help', self)
        self.help_action.triggered.connect(self.show_help)

        self.conf_action = QAction('&Configure', self)
        self.conf_action.triggered.connect(self.show_configure)

        self.main_menu = self.menuBar()
        self.settings_menu = self.main_menu.addMenu('&Settings')
        self.settings_menu.addAction(self.conf_action)
        self.settings_menu.addAction(self.help_action)

    def show_files_dialog(self):
        self.data_fname = QFileDialog.getOpenFileName(self, 'Choose data file',
                                                      filter="ECG format files "
                                                             "(*.txt *.ecg *.cmp *.ano *.edf *.hea *.atr *.dat)")[0]
        self.data_fname_label.setText(self.data_fname[self.data_fname.rfind('/') + 1:]
                                      if self.data_fname != '' else 'No file chosen')
        self.classify_button.setEnabled(self.data_fname != '')

    def plot_results(self):
        pred_classes, signals, fields, qrs_inds = self.analysis.analyze(self.data_fname)

        self.canvas = PlotCanvas(width=len(signals) // 120, height=FIG_H * signals.shape[1])
        self.canvas.plot_analysis_res(signals, fields, pred_classes, qrs_inds)

        self.removeToolBar(self.nav_toolbar)
        self.nav_toolbar = NavigationToolbar(self.canvas, self)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.nav_toolbar)

        self.scroll_area.setWidget(self.canvas)
        self.scroll_area.setMinimumHeight(
            FIG_H * min(signals.shape[1], 2) * DPI + self.scroll_area.horizontalScrollBar().sizeHint().height() + 2)
        self.scroll_area.setAlignment(Qt.AlignTop)

    @staticmethod
    def show_configure():
        conf_dialog = ConfDialog()
        conf_dialog.exec()

    @staticmethod
    def show_help():
        pass


class ConfDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cygwin configuration')
        self.setSize()
        self.initUI()

    def setSize(self):
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.explain_label = QLabel(BASH_CONF_MSG)
        self.explain_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.choose_bash_button = QPushButton('Choose file')
        self.choose_bash_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.choose_bash_button.clicked.connect(self.show_files_dialog)

        text_for_label = 'No file chosen'
        if os.path.exists(BASH_PATH_FNAME):
            with open(BASH_PATH_FNAME, 'r') as fin:
                path = fin.read().strip()
            if path != '':
                text_for_label = path

        self.bash_fname_label = QLabel(text_for_label)
        self.bash_fname_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.bash_fname_label.setAlignment(Qt.AlignVCenter)

        self.file_hlayout = QHBoxLayout()
        self.file_hlayout.setAlignment(Qt.AlignTop)
        self.file_hlayout.addWidget(self.choose_bash_button)
        self.file_hlayout.addWidget(self.bash_fname_label)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.explain_label)
        self.layout.addLayout(self.file_hlayout)

        self.setLayout(self.layout)

    def show_files_dialog(self):
        self.bash_fname = QFileDialog.getOpenFileName(self, 'Choose cygwin bash file',
                                                      filter="bash.exe")[0]
        self.bash_fname_label.setText(self.bash_fname
                                      if self.bash_fname != '' else 'No file chosen')

        with open(BASH_PATH_FNAME, 'w') as fout:
            fout.write(self.bash_fname)


class WarningMessage(QMessageBox):
    def __init__(self, message, title='Warning'):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(QMessageBox.Warning)
        self.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Appication()
    sys.exit(app.exec_())
