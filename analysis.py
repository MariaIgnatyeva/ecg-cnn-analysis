import subprocess

from constants import *
from app import WarningMessage, Appication
from model import ECGModel
import os
import wfdb
from wfdb import processing


class CNNAnalysis():
    def __init__(self, status_bar=None):
        self.status_bar = status_bar
        self.model = ECGModel(MODEL_FNAME)

    def is_conf_error(self):
        is_bash_error = False

        if os.path.exists(BASH_PATH_FNAME):
            with open(BASH_PATH_FNAME, 'r') as fin:
                self.bash_fname = fin.read().strip()
            if not os.path.exists(self.bash_fname):
                is_bash_error = True
        else:
            is_bash_error = True

        if is_bash_error:
            WarningMessage(BASH_CONF_ERR_MSG)
            Appication.show_configure()

        return is_bash_error

    def convert_to_mit(self, ext):
        try:
            wfdb_cmd = 'ahaecg2mit' if ext in AHA_EXT else 'edf2mit -i'
            convert_cmd = 'cd \'' + self.data_fname[:self.data_fname.rfind('/')] + '\'\n' \
                          + wfdb_cmd + ' ' + self.data_fname[self.data_fname.rfind('/') + 1:]

            p = subprocess.Popen(self.bash_fname[:-4] + " -l",
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.stdin.write(bytes(convert_cmd, 'utf-8'))
            p.stdin.close()
            o, e = p.communicate()

            error_msg = CONVERT_ERR_MSG if p.returncode != 0 else ''
            WarningMessage(e.decode('utf-8')[:-1] + error_msg, 'Conversion result')
        except BaseException:
            return 1

        return p.returncode != 0

    def read_data(self):
        record_name = self.data_fname[:-4]
        ext = self.data_fname[-3:]

        if ext not in MITBIH_EXT:
            if self.is_conf_error() or self.convert_to_mit(ext):
                return 1

        elif not (os.path.exists(record_name + '.dat') and os.path.exists(record_name + '.hea')):
            WarningMessage(MIT_ERR_MSG)
            return 1

        signals, fields = wfdb.rdsamp(record_name, sampto=7000)
        if ext in EDF_EXT:
            signals = signals[:, :-1]

        return fields, signals

    def get_qrs_inds(self, signals, fs):
        qrs_inds = processing.correct_peaks(signals[:, 0],
                                            processing.xqrs_detect(signals[:, 0], fs,
                                                                   conf=processing.XQRS.Conf(hr_min=20, hr_max=230,
                                                                                             qrs_width=0.5)),
                                            fs * 60 // 230,
                                            fs // 2,
                                            'compare')

        return qrs_inds

    def get_predictions(self, signals, qrs_inds):
        r = self.model.predict(signals, qrs_inds)
        print(r[:10])
        return r

    def analyze(self, data_fname):
        self.data_fname = data_fname
        read_data_res = self.read_data()
        if not isinstance(read_data_res, tuple):
            return None

        fields, signals = read_data_res
        fs = fields['fs']

        qrs_inds = self.get_qrs_inds(signals, fs)

        preds = self.get_predictions(signals, qrs_inds)
        return preds, signals, fields, qrs_inds
