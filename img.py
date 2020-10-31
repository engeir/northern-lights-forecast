"""This script finds all pixels with colour within a range a colours, while all other is coloured black.
From https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
"""

import os
import wget
import numpy as np
import cv2
import pytesseract


def download():
    """Download a `.gif` file, save and return as `.jpg`.

    Returns:
        cv2 image: the downloaded file as `.jpg`
    """
    file = 'Last24_tro2a.gif'
    if os.path.exists(file):
        os.remove(file)

    url = 'https://flux.phys.uit.no/Last24/Last24_tro2a.gif'
    wget.download(url, out='assets/Last24_tro2a.gif')

    gif = cv2.VideoCapture('assets/Last24_tro2a.gif')
    ret, frame = gif.read()
    cv2.imwrite('assets/images.jpg', frame)
    image = cv2.imread('assets/images.jpg')

    return image


def read(image):
    """Read the scaling of the axis of the downloaded file.
    See `download()`.

    Args:
        image (cv2 image): the input file

    Returns:
        float: scaling factor of y axis to pixels
    """
    if True:
        images = np.hstack([image[360:530, 1:40, :]])
        data=pytesseract.image_to_boxes(images)

        d = data.split('\n')
        d = [data for data in d if len(data) > 1]
        d = d[::-1]
        # print(d)
        c = 0
        lim_0 = ''
        y_0 = ''
        lim_1 = ''
        y_1 = ''
        for l in d:
            l = l.split()
            if l[0] == '-':
                c += 1
            else:
                if c == 0:
                    lim_0 += l[0]
                    y_0 = l[2]
                elif c == 1:
                    lim_1 += l[0]
                    y_1 = l[2]
            if c >= 2:
                break
        lim_0 = float(lim_0[::-1])
        y_b = float(y_0)
        lim_1 = float(lim_1[::-1])
        y_t = float(y_1)
        # print(lim_0, lim_1, y_b, y_t)
        # print(round(abs(lim_1 - lim_0) / abs(y_t - y_b), 2))
        # import matplotlib.pyplot as plt
        # plt.figure()
        # plt.imshow(images)
        # plt.show()
    else:
        x_0, x_1 = 1, 40
        y_t0, y_t1 = 360, 390
        y_b0, y_b1 = 455, 485
        y_t, y_b = 380, 475
        txt_img0 = np.hstack([image[y_t0:y_t1, x_0:x_1, :]])
        txt_img1 = np.hstack([image[y_b0:y_b1, x_0:x_1, :]])
        # Uncomment block below to verify the text is completely inside the images.
        # # === < View y axis text > ===
        # import matplotlib.pyplot as plt
        # plt.figure()
        # plt.imshow(txt_img0)
        # plt.figure()
        # plt.imshow(txt_img1)
        # plt.show()
        # exit()
        # # === </ View y axis text > ===
        # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
        # we need to convert from BGR to RGB format/mode:
        img_rgb0 = cv2.cvtColor(txt_img0, cv2.COLOR_BGR2RGB)
        img_rgb1 = cv2.cvtColor(txt_img1, cv2.COLOR_BGR2RGB)
        lim_0 = float(pytesseract.image_to_string(img_rgb0))
        lim_1 = float(pytesseract.image_to_string(img_rgb1))
    # print(f'Pixels to nT: {abs(y_t - y_b)} to {abs(lim_1 - lim_0)}')
    # print(f'Increase by {round(abs(lim_1 - lim_0) / abs(y_t - y_b), 2)} times')
    return round(abs(lim_1 - lim_0) / abs(y_t - y_b), 2)


def find_colour(image):
    """Find the pixels in an image with colour within a given range.

    Args:
        image (cv2 image): the input file
    """
    # Define the list of boundaries
    boundaries = [
        # ([17, 15, 100], [50, 56, 200]),  # red
        ([86, 4, 4], [255, 100, 100])  # blue
        # ([25, 146, 190], [62, 174, 250]),  # yellow
        # ([103, 86, 65], [145, 133, 128])  # grey
    ]

    # Loop over the boundaries
    # for (lower, upper) in boundaries:
    lower, upper = boundaries[0]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # Find the colors within the specified boundaries and apply
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    # Set the masked pixels to white
    output[output > 0] = 255

    # # === < Show figures > ===
    # import matplotlib.pyplot as plt
    # plt.figure()
    # plt.imshow(image)
    # # plt.savefig('before.png', dpi=200)
    # # plt.figure()
    # # plt.imshow(output)
    # # plt.show()
    # # === </ Show figures > ===
    # Save the black/white image of the blue structures
    cv2.imwrite('assets/new_im.jpg', np.hstack([output]))


def main():
    # Download image
    image = download()
    scaling = read(image)
    # Crop image
    y_h = int(image.shape[0] * .4)
    x_h = int(image.shape[1] * .1)
    image = np.hstack([image[y_h:, x_h:, :]])

    # Find colour of a given image and set to white,
    # the rest is set to black. Then save.
    find_colour(image)

    return scaling


if __name__ == '__main__':
    main()
