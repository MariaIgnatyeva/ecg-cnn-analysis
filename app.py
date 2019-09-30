import sys

from PyQt5.QtCore import Qt

import os
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QSizePolicy, QScrollArea, QMainWindow, \
    QVBoxLayout, QLabel, QHBoxLayout, QWidget, QApplication, QAction, QDialog, QPushButton, \
    QMessageBox, QGridLayout, QGroupBox, QStyle
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from constants import *
import analysis
from canvas import PlotCanvas

analysis_obj = None


class Appication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.initUI()

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
        self.classify_button.setEnabled(False)
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

        self.scroll_area = QScrollArea()
        self.scroll_area.setAlignment(Qt.AlignTop)
        self.scroll_area.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        self.scroll_area.setFixedHeight(
            int(FIG_H * DPI) + self.scroll_area.horizontalScrollBar().sizeHint().height() + 2)
        self.scroll_area.setWidget(self.canvas)

        self.stat_results_group = QGroupBox('Classification results')
        self.init_stat_results()
        self.stat_results_group.setLayout(self.stat_results_layout)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.addLayout(self.pred_hlayout)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.stat_results_group)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.statusBar()
        self.showMaximized()

    def init_stat_results(self):
        self.stat_results_layout = QGridLayout()
        self.stat_results_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.stat_results_labels = {'nor': QLabel('NOR - normal beats:'),
                                    'pab': QLabel('PAB - paced beats:'),
                                    'vfw': QLabel('VFW - ventricular flutter wave beats:'),
                                    'veb': QLabel('VEB - ventricular escape beats:'),
                                    'rbb': QLabel('RBB - right bundle branch block beats:'),
                                    'lbb': QLabel('LBB - left bundle branch block beats:'),
                                    'pvc': QLabel('PVC - premature ventricular contraction beats:'),
                                    'apc': QLabel('APC - atrial premature contraction beats:')}
        self.stat_results_counts = dict(zip(self.stat_results_labels.keys(),
                                            [QLabel('-') for i in range(len(self.stat_results_labels.keys()))]))

        ind = 0
        for c, label in self.stat_results_labels.items():
            self.stat_results_labels[c].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.stat_results_layout.addWidget(label, ind % 4, ind // 4 * 2, Qt.AlignRight)

            self.stat_results_counts[c].setContentsMargins(0, 0, 120, 0)
            self.stat_results_layout.addWidget(self.stat_results_counts[c], ind % 4, (ind // 4 * 2) + 1)
            ind += 1

    def resume_stat_results(self):
        ind = 0
        for c, _ in self.stat_results_labels.items():
            self.stat_results_counts[c].setText('-')
            ind += 1

    def set_stat_results(self, pred_classes):
        classes, counts = np.unique(pred_classes, return_counts=True)
        for i, c in enumerate(classes):
            self.stat_results_counts[c].setText(str(counts[i]))

    def init_menu(self):
        self.conf_action = QAction('&Configure', self)
        self.conf_action.triggered.connect(self.show_configure)

        self.main_menu = self.menuBar()
        self.settings_menu = self.main_menu.addMenu('&Settings')
        self.settings_menu.addAction(self.conf_action)

    def show_files_dialog(self):
        self.data_fname = QFileDialog.getOpenFileName(self, 'Choose data file',
                                                      filter="ECG format files "
                                                             "(*.txt *.ecg *.cmp *.ano *.edf *.hea *.atr *.dat)")[0]
        self.data_fname_label.setText(self.data_fname[self.data_fname.rfind('/') + 1:]
                                      if self.data_fname != '' else 'No file chosen')
        self.classify_button.setEnabled(self.data_fname != '')

    def define_analysis(self):
        global analysis_obj

        if analysis_obj is None:
            analysis_obj = analysis.CNNAnalysis(self.statusBar())
            self.statusBar().showMessage('Model loaded, ready to classify')

    def plot_results(self):
        self.classify_button.setEnabled(False)
        self.resume_stat_results()

        self.statusBar().showMessage('Predicting...')
        pred_classes, signals, fields, qrs_inds = analysis_obj.analyze(self.data_fname)

        self.canvas = PlotCanvas(width=len(signals) // 120, height=FIG_H * signals.shape[1])
        self.canvas.plot_analysis_res(signals, fields, pred_classes, qrs_inds)

        self.removeToolBar(self.nav_toolbar)
        self.nav_toolbar = NavigationToolbar(self.canvas, self)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.nav_toolbar)

        self.scroll_area.setWidget(self.canvas)
        self.scroll_area.setFixedHeight(min(
            self.height() - self.statusBar().height() - \
            self.nav_toolbar.sizeHint().height() - self.stat_results_layout.sizeHint().height() - \
            self.pred_hlayout.sizeHint().height() - self.menuBar().height() - \
            QApplication.style().pixelMetric(QStyle.PM_TitleBarHeight) - 25,
            int(FIG_H * DPI * signals.shape[1]) + self.scroll_area.horizontalScrollBar().sizeHint().height() + 2))

        self.set_stat_results(pred_classes)
        self.statusBar().showMessage('Predicting completed, ready to classify')

    def show_stat_results(self):
        pass

    @staticmethod
    def show_configure():
        ConfDialog()


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
        self.bash_fname_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
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
        self.exec()

    def show_files_dialog(self):
        self.bash_fname = QFileDialog.getOpenFileName(self, 'Choose cygwin bash file',
                                                      filter="bash.exe")[0]
        self.bash_fname_label.setText(self.bash_fname
                                      if self.bash_fname != '' else 'No file chosen')

        with open(BASH_PATH_FNAME, 'w') as fout:
            fout.write(self.bash_fname)


class WarningMessage(QMessageBox):
    def __init__(self, message, buttons=None, title='Warning'):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(QMessageBox.Warning)
        if buttons == QMessageBox.NoButton:
            self.setStandardButtons(buttons)
        self.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Appication()
    window.define_analysis()
    sys.exit(app.exec_())
