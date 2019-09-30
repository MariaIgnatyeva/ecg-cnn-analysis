from keras.models import load_model
from generators import predict_iterator
from constants import *
import keras.backend as K
import numpy as np


def f1(y_true, y_pred):
    def recall(y_true, y_pred):
        """Recall metric.

        Only computes a batch-wise average of recall.

        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())

        return recall

    def precision(y_true, y_pred):
        """Precision metric.

        Only computes a batch-wise average of precision.

        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())

        return precision

    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    f1_val = 2 * ((precision * recall) / (precision + recall + K.epsilon()))

    return f1_val


class ECGModel:
    def __init__(self, path_to_model):
        print('loading model...')
        self.model = load_model(path_to_model, custom_objects={'f1': f1})
        print('model loaded')

    def predict(self, signals, qrs_inds):
        print('predicting...')
        preds = self.model.predict_generator(predict_iterator(signals[:, 0], qrs_inds), steps=len(qrs_inds), verbose=1)
        print('predicting completed...')
        pred_inds = np.argmax(preds, axis=1)

        return [IDX_TO_CLASS[ind] for ind in pred_inds]
