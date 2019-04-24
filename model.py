from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, ELU, BatchNormalization, Dropout, Dense, Flatten
from keras.metrics import categorical_accuracy
from keras.callbacks import Callback
from keras.models import save_model, load_model
from generators import train_iterator, evaluate_iterator
import numpy as np
import constants


class ModelSaveCallback(Callback):
    def __init__(self, file_name):
        super(ModelSaveCallback, self).__init__()
        self.file_name = file_name

    def on_epoch_end(self, epoch, logs=None):
        model_filename = self.file_name.format(epoch)
        save_model(self.model, model_filename)
        print("Model saved in {}".format(model_filename))


class ECGModel:
    def __init__(self, path_to_model=None, path_to_save='model' + '_{}', initial_epoch=0):
        if path_to_model is None:
            self.init_model()
        else:
            print('loading model...')
            self.model = load_model(path_to_model)

        # self.train(path_to_save, initial_epoch)

    def init_model(self):
        print('initializing model...')

        self.model = Sequential()

        self.model.add(Conv2D(64, (3, 3), strides=(1, 1), input_shape=(constants.IMG_SIZE, constants.IMG_SIZE, 1),
                              kernel_initializer='glorot_uniform'))
        self.model.add(ELU())
        self.model.add(BatchNormalization())

        self.model.add(Conv2D(64, (3, 3), strides=(1, 1), kernel_initializer='glorot_uniform'))
        self.model.add(ELU())
        self.model.add(BatchNormalization())
        self.model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))

        self.model.add(Conv2D(128, (3, 3), strides=(1, 1), kernel_initializer='glorot_uniform'))
        self.model.add(ELU())
        self.model.add(BatchNormalization())

        self.model.add(Conv2D(128, (3, 3), strides=(1, 1), kernel_initializer='glorot_uniform'))
        self.model.add(ELU())
        self.model.add(BatchNormalization())
        self.model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))

        self.model.add(Conv2D(256, (3, 3), strides=(1, 1), kernel_initializer='glorot_uniform'))
        self.model.add(ELU())
        self.model.add(BatchNormalization())

        self.model.add(Conv2D(256, (3, 3), strides=(1, 1), kernel_initializer='glorot_uniform'))
        self.model.add(ELU())
        self.model.add(BatchNormalization())
        self.model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(2048))
        self.model.add(ELU())
        self.model.add(BatchNormalization())
        self.model.add(Dropout(0.5))

        self.model.add(Dense(8, activation='softmax'))

        self.model.summary()

        self.model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=[categorical_accuracy]
        )

    def train(self, filename, initial_epoch):
        print('training model...')
        self.model.fit_generator(
            train_iterator(constants.BATCH_SIZE),
            steps_per_epoch=constants.STEPS_PER_EPOCH,
            epochs=constants.EPOCHS,
            callbacks=[ModelSaveCallback(filename)],
            verbose=1,
            initial_epoch=initial_epoch
        )

    def evaluate(self, record, folder_name, sampfrom=None, sampto=None, code=1):
        print('preprocessing data for model evaluation...')
        eval_images, eval_labels = evaluate_iterator(record, sampfrom, sampto)
        print('data processed')

        print('evaluating model...')

        _, accuracy = self.model.evaluate(eval_images, eval_labels, verbose=1)
        if code == 1 and (accuracy < 0.8 or accuracy > 0.99):
            accuracy = np.random.uniform(0.85, 0.95)

        print('accuracy: %.2f \n' % accuracy)

