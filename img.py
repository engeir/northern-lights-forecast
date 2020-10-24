"""This script finds all pixels with colour within a range a colours them white, while all other is coloured black.
From https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
"""

import os
# import argparse
import wget
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pytesseract

def download():
    file = 'Last24_tro2a.gif'
    if os.path.exists(file):
        os.remove(file)

    url = 'https://flux.phys.uit.no/Last24/Last24_tro2a.gif'
    wget.download(url)


def read(image):
    x_0 = 1
    x_1 = 40
    y_t0 = 370
    y_t1 = 390
    y_b0 = 465
    y_b1 = 485
    y_t = 380
    y_b = 475
    txt_img0 = np.hstack([image[y_t0:y_t1, x_0:x_1, :]])
    txt_img1 = np.hstack([image[y_b0:y_b1, x_0:x_1, :]])
    # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
    # we need to convert from BGR to RGB format/mode:
    img_rgb0 = cv2.cvtColor(txt_img0, cv2.COLOR_BGR2RGB)
    img_rgb1 = cv2.cvtColor(txt_img1, cv2.COLOR_BGR2RGB)
    lim_0 = float(pytesseract.image_to_string(img_rgb0))
    lim_1 = float(pytesseract.image_to_string(img_rgb1))
    # print(f'Pixels to nT: {abs(y_t - y_b)} to {abs(lim_1 - lim_0)}')
    # print(f'Increase by {round(abs(lim_1 - lim_0) / abs(y_t - y_b), 2)} times')
    return round(abs(lim_1 - lim_0) / abs(y_t - y_b), 2)

def main():
    download()
    # image = cv2.imread('Last24_tro2a.gif')
    gif = cv2.VideoCapture('Last24_tro2a.gif')
    ret, frame = gif.read()
    cv2.imwrite('images.jpg', frame)
    image = cv2.imread('images.jpg')
    y_h = int(image.shape[0] * .4)
    x_h = int(image.shape[1] * .1)
    scaling = read(image)
    image = np.hstack([image[y_h:, x_h:, :]])

    # define the list of boundaries
    boundaries = [
        # ([17, 15, 100], [50, 56, 200]),  # red
        ([86, 4, 4], [255, 100, 100])  # blue
        # ([25, 146, 190], [62, 174, 250]),  # yellow
        # ([103, 86, 65], [145, 133, 128])  # grey
    ]

    # print(image[image!=[250, 250, 250]].shape)
    # print(np.unique(image, axis=0, return_counts=True))

    # loop over the boundaries
    # for (lower, upper) in boundaries:
    lower, upper = boundaries[0]
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    # print(np.max(output))
    output[output > 0] = 255
    # plt.figure()
    # plt.imshow(image)
    # plt.figure()
    # plt.imshow(output)
    # plt.show()
    # show the images
    cv2.imwrite('new_im.jpg', np.hstack([output]))
    # cv2.imshow("images", np.hstack([image, output]))
    # cv2.waitKey(0)
    return scaling


if __name__ == '__main__':
    main()
