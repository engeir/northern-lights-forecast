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
    wget.download(url)

    gif = cv2.VideoCapture('Last24_tro2a.gif')
    ret, frame = gif.read()
    cv2.imwrite('images.jpg', frame)
    image = cv2.imread('images.jpg')

    return image


def read(image):
    """Read the scaling of the axis of the downloaded file.
    See `download()`.

    Args:
        image (cv2 image): the input file

    Returns:
        float: scaling factor of y axis to pixels
    """
    x_0, x_1 = 1, 40
    y_t0, y_t1 = 370, 390
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
    cv2.imwrite('new_im.jpg', np.hstack([output]))


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
