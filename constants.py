SYM_TO_CLASS = {'N': 'nor', 'L': 'lbb', 'R': 'rbb', 'A': 'apc',
                'V': 'pvc', '/': 'pab', 'E': 'veb', '!': 'vfw'}
CLASS_TO_IDX = {'nor': 1, 'lbb': 2, 'rbb': 5, 'apc': 0, 'pvc': 4, 'pab': 3, 'veb': 6, 'vfw': 7}
IDX_TO_CLASS = dict(zip(CLASS_TO_IDX.values(), CLASS_TO_IDX.keys()))

MITBIH_EXT = ['dat', 'hea', 'atr']
AHA_EXT = ['txt', 'ecg', 'cmp', 'ano']
EDF_EXT = ['edf']

FIG_W = 30
FIG_H = 3
DPI = 100

APP_TITLE = 'Heart Arrhythmia Classification Using Neural Network'

BASH_PATH_FNAME = 'bash_path.txt'
MODEL_FNAME = 'model'
CONVERT_ERR_MSG = '\nSomething went wrong during conversion, check cygwin configuration and if the file is correct'
BASH_CONF_MSG = 'To analyze data not in MIT-BIH format cygwin is required\n' + \
                'Choose bash.exe, usually it\'s path is cygwin/bin/bash.exe'
BASH_CONF_ERR_MSG = 'Cygwin is not properly configured. Choose bash.exe and try to classify again'
MIT_ERR_MSG = '.dat or .hea file not found'

MV = 10
