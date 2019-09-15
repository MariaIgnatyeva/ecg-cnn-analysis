import cv2
import numpy as np
from preprocessing import signal_to_image


def predict_iterator(signals, qrs_inds, folder_name='pred'):
    for i in range(len(qrs_inds)):
        left_ind = 0 if i == 0 else qrs_inds[i - 1] + 20
        right_ind = len(signals) if i == len(qrs_inds) - 1 else qrs_inds[i + 1] - 20
        signal = signals[left_ind: right_ind]
        signal_to_image(signal, folder_name)

        image = cv2.imread(folder_name + '/0_0.png', cv2.IMREAD_GRAYSCALE)
        image = np.expand_dims(image, -1)

        yield np.expand_dims(image, 0)
