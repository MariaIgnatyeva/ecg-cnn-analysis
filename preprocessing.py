import matplotlib.pyplot as plt
import cv2
import os

def signal_to_image(signal, folder_name, record_ind=0, signal_ind=0):
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
