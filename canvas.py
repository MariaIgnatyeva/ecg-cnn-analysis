from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MultipleLocator
import numpy as np

from constants import *
from matplotlib.figure import Figure


class PlotCanvas(FigureCanvas):
    def __init__(self, width=FIG_W, height=FIG_H, dpi=DPI):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_tight_layout(True)
        super().__init__(self.fig)

        self.init_axes()

        FigureCanvas.setSizePolicy(self, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

    def init_axes(self):
        self.axes = []

        channels_n = int(self.fig.get_figheight() / FIG_H)
        self.axes.append(self.fig.add_subplot(channels_n, 1, 1))
        for i in range(1, channels_n):
            self.axes.append(self.fig.add_subplot(channels_n, 1, i + 1, sharex=self.axes[0]))

    def set_axes_grid_label(self, ch_n, sig_names, units):
        self.axes[ch_n].xaxis.set_major_locator(MultipleLocator(0.2))
        self.axes[ch_n].xaxis.set_minor_locator(MultipleLocator(0.04))
        self.axes[ch_n].yaxis.set_major_locator(MultipleLocator(5 / MV))
        self.axes[ch_n].yaxis.set_minor_locator(MultipleLocator(1 / MV))

        self.axes[ch_n].grid(True, which='major', linewidth=1, color='r', alpha=0.15)
        self.axes[ch_n].grid(True, which='minor', linewidth=0.5, color='r', alpha=0.15)

        self.axes[ch_n].set_ylabel(sig_names[ch_n] + '/' + units[ch_n])

    def set_lims(self, min_mv, max_mv, max_time):
        self.axes[0].set_ylim(min_mv - 0.1, max_mv + 3.5 * (max_mv - min_mv) / MV)
        self.axes[0].set_xlim(0, max_time)

    def annotate_fs_mv(self, fs, x, min_mv, max_mv):
        self.axes[0].annotate(str(int(fs)) + ' samples/sec', (x, max_mv + 2.5 * (max_mv - min_mv) / MV),
                              color='k', fontsize=12)
        self.axes[0].annotate(str(int(MV)) + ' mm/mV', (x, max_mv + 1.5 * (max_mv - min_mv) / MV),
                              color='k', fontsize=12)

    def annotate_preds(self, preds, qrs_inds, time, min_mv, max_mv):
        for i, ind in enumerate(qrs_inds):
            color = 'b' if preds[i] == 'nor' else 'r'
            self.fig.axes[0].annotate(preds[i].upper(),
                                      (time[ind], max_mv + 0.5 * (max_mv - min_mv) / MV),
                                      color=color, fontsize=12)

    def set_axes(self, min_mv, max_mv, max_time, fs, ind_fs_mv):
        self.axes[-1].set_xlabel('time/seconds')
        self.set_lims(min_mv, max_mv, max_time)
        self.annotate_fs_mv(fs, ind_fs_mv, min_mv, max_mv)
        self.fig.set_tight_layout(True)

    def plot_analysis_res(self, signals, fields, preds, qrs_inds):
        min_mv = min(signals[:, 0])
        max_mv = max(signals[:, 0])

        time = np.linspace(0, len(signals) / fields['fs'], len(signals))

        for ch_n in range(signals.shape[1] if len(signals.shape) == 2 else 1):
            self.set_axes_grid_label(ch_n, fields['sig_name'], fields['units'])
            self.axes[ch_n].plot(time, signals[:, ch_n], color='k')
        self.annotate_preds(preds, qrs_inds, time, min_mv, max_mv)

        self.set_axes(min_mv, max_mv, max(time), fields['fs'], time[15])
        self.draw()
