import cv2
import wfdb
import constants
import numpy as np
import glob
from keras.utils import to_categorical
from preprocessing import signal_to_image

all_paths = glob.glob('./' + constants.FOLDER_NAME + '/*.png')

number_to_label = {}
with open('number_label.txt', 'r') as f:
    for line in f:
        n, l = line.split()
        number_to_label[n] = int(l)

# all_labels = np.zeros(len(all_paths), dtype='int')
# with open('labels.txt', 'r') as f:
#     for i in range(len(all_labels)):
#         all_labels[i] = constants.CLASS_TO_IDX[f.readline()[:-1]]

nor_class_ind = np.where(np.array(list(number_to_label.values())) == constants.CLASS_TO_IDX['nor'])[0]
np.random.shuffle(nor_class_ind)
ind_to_delete = nor_class_ind[np.arange(8000, len(nor_class_ind))]

paths = np.delete(all_paths, ind_to_delete)

batch_i = 0
indices = np.arange(0, len(paths))
np.random.shuffle(indices)


def get_cropping_images(image):
    left_top = cv2.resize(image[:96, :96], (constants.IMG_SIZE, constants.IMG_SIZE))
    center_top = cv2.resize(image[:96, 16:112], (constants.IMG_SIZE, constants.IMG_SIZE))
    right_top = cv2.resize(image[:96, 32:], (constants.IMG_SIZE, constants.IMG_SIZE))

    left_center = cv2.resize(image[16:112, :96], (constants.IMG_SIZE, constants.IMG_SIZE))
    center_center = cv2.resize(image[16:112, 16:112], (constants.IMG_SIZE, constants.IMG_SIZE))
    right_center = cv2.resize(image[16:112, 32:], (constants.IMG_SIZE, constants.IMG_SIZE))

    left_bottom = cv2.resize(image[32:, :96], (constants.IMG_SIZE, constants.IMG_SIZE))
    center_bottom = cv2.resize(image[32:, 16:112], (constants.IMG_SIZE, constants.IMG_SIZE))
    right_bottom = cv2.resize(image[32:, 32:], (constants.IMG_SIZE, constants.IMG_SIZE))

    return np.array([left_top, center_top, right_top,
                     left_center, center_center, right_center,
                     left_bottom, center_bottom, right_bottom])


def get_generator(ind, augment=False):
    image = cv2.imread(paths[ind], cv2.IMREAD_GRAYSCALE)
    number_path = paths[ind][paths[ind].find('\\') + 1: paths[ind].rfind('.')]
    label = number_to_label[number_path]

    if augment:
        cropped_images = get_cropping_images(image)
        images = np.vstack((np.expand_dims(image, axis=0), cropped_images))
        yield images, np.full(len(images), label)
    else:
        yield image, label


def raw_batch_generator(batch_size, augment=False, debug=False):
    global batch_i

    generators = np.array([get_generator(ind, augment) for ind in range(len(paths))])
    while True:
        batch_i += 1
        batch_indices = indices[batch_i * batch_size: (batch_i + 1) * batch_size]
        yield [gen.__next__() for gen in generators[batch_indices]]


def images_and_labels_generator(batch_size, augment=False):
    for batch in raw_batch_generator(batch_size, augment):
        batch_images = []
        batch_labels = []
        for e in batch:
            batch_images.append(e[0])
            batch_labels.append(e[1])
        batch_images = np.stack(batch_images, axis=0) if not augment else np.vstack(batch_images)
        yield batch_images, batch_labels


def train_iterator(batch_size, augment=False):
    for batch in images_and_labels_generator(batch_size, augment):
        batch_images = batch[0]
        batch_images = np.expand_dims(batch_images, -1)
        batch_labels = to_categorical(batch[1], constants.NUM_CLASSES)
        yield batch_images, batch_labels


def evaluate_iterator(record, sampfrom, sampto, folder_name='eval'):
    eval_images = []
    eval_labels = []
    record_ind = 0
    signal_ind = 0

    signals = wfdb.rdsamp(record, channels=[0], sampfrom=sampfrom, sampto=sampto, pb_dir='mitdb')[0]
    ann = wfdb.rdann(record, 'atr', sampfrom=sampfrom, sampto=sampto, pb_dir='mitdb')
    symbols = ann.symbol
    beats = list(ann.sample)

    for i in range(2, len(beats) - 1):
        if symbols[i] in list(constants.SYM_TO_CLASS.keys()):
            signal = signals[beats[i - 1] + 20: beats[i + 1] - 20, 0]
            signal_to_image(signal, folder_name, 0, 0)

            image = cv2.imread(folder_name + '/' + str(record_ind) + '_' + str(signal_ind) + '.png',
                               cv2.IMREAD_GRAYSCALE)
            image = np.expand_dims(image, -1)
            eval_images.append(image)

            label = to_categorical(constants.CLASS_TO_IDX[constants.SYM_TO_CLASS[symbols[i]]], constants.NUM_CLASSES)
            eval_labels.append(label)

    eval_images = np.stack(eval_images, axis=0)
    eval_labels = np.stack(eval_labels, axis=0)
    return eval_images, eval_labels
