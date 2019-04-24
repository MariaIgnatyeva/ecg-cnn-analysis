import matplotlib.pyplot as plt
import cv2
import wfdb
import os
import constants


def signal_to_image(signal, folder_name, record_ind, signal_ind):
    fig = plt.figure(frameon=False)
    plt.plot(signal, linewidth=3.5)
    plt.xticks([]), plt.yticks([])
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    filename = folder_name + '/' + str(record_ind) + '_' + str(signal_ind) + '.png'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    fig.savefig(filename)
    im_gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    im_gray = cv2.resize(im_gray, (128, 128))
    cv2.imwrite(filename, im_gray)

    plt.close(fig)

    return im_gray


def generate_images(records, folder_name, sampto=None):
    signal_ind = 0

    for record_ind, record in enumerate(records):
        signals = wfdb.rdsamp(record, channels=[0], sampto=sampto, pb_dir='mitdb')[0]
        ann = wfdb.rdann(record, 'atr', sampto=sampto, pb_dir='mitdb')
        symbols = ann.symbol
        beats = list(ann.sample)

        for i in range(2, len(beats) - 1):
            if symbols[i] in list(constants.SYM_TO_CLASS.keys()):
                #             left_diff = abs(beats[i - 1] - beats[i]) // 2
                #             right_diff = abs(beats[i + 1] - beats[i]) // 2
                signal = signals[beats[i - 1] + 20: beats[i + 1] - 20, 0]

                # segmented_signals.append(signal)
                # label_to_ind[constants.SYM_TO_CLASS[symbols[i]]].append(len(segmented_signals) - 1)

                signal_to_image(signal, folder_name, record_ind, signal_ind)
                signal_ind += 1

                # with open('segmented_signals.txt', 'a') as f:
                #     np.savetxt(f, signal, delimiter=',')
                #     f.write('\n')

                with open('labels.txt', 'a' if not os.path.exists('labels.txt') else 'w') as f:
                    f.write(constants.SYM_TO_CLASS[symbols[i]])
                    f.write('\n')

        print('images generated for record', record_ind)
