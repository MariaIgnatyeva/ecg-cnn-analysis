NUM_CLASSES = 8
IMG_SIZE = 128
BATCH_SIZE = 32
STEPS_PER_EPOCH = 90
EPOCHS = 14
FOLDER_NAME = 'signals_20'

SYM_TO_CLASS = {'N': 'nor', 'L': 'lbb', 'R': 'rbb', 'A': 'apc',
                'V': 'pvc', '/': 'pab', 'E': 'veb', '!': 'vfw'}
CLASS_TO_IDX = {'nor': 1, 'lbb': 2, 'rbb': 5, 'apc': 0, 'pvc': 4, 'pab': 3, 'veb': 6, 'vfw': 7}
IDX_TO_CLASS = dict(zip(CLASS_TO_IDX.values(), CLASS_TO_IDX.keys()))