"""Sort out colours from an image.

This script finds all pixels with colour within a range a colours, while all
other is coloured black. From
https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
"""
import os

import cv2
import numpy as np
import pytesseract
import wget

# import matplotlib.pyplot as plt

PLACE = {
    "Ny-Ålesund": "nal1a",
    "Tromsø": "tro2a",
    "Longyearbyen": "lyr2a",
    "Hopen": "hop1a",
    "Bjørnøya": "bjn1a",
    "Jan Mayen": "jan1a",
    "Nordkapp": "nor1a",
    "Andenes": "and1a",
    "Røst": "rst1a",
    "Jackvik": "jck1a",
    "Dønna": "don1a",
    "Rørvik": "rvk1a",
    "Dombås": "dob1a",
    "Solund": "sol1a",
    "Harestua": "har1a",
    "Karmøy": "kar1a",
}


def download() -> np.ndarray:
    """Download a `.gif` file, save and return as `.jpg`.

    Returns
    -------
    np.ndarray:
        the downloaded file as `.jpg`
    """
    file = "assets/Last24_tro2a.gif"
    if os.path.exists(file):
        os.remove(file)

    url = "https://flux.phys.uit.no/Last24/Last24_tro2a.gif"
    # saveas = "down.gif"
    # wget.download(url, out="assets/saveas")
    wget.download(url, out="assets/Last24_tro2a.gif")

    # gif = cv2.VideoCapture("assets/saveas")
    gif = cv2.VideoCapture("assets/Last24_tro2a.gif")
    ret, frame = gif.read()
    cv2.imwrite("assets/images.jpg", frame)
    image = cv2.imread("assets/images.jpg")

    return image


def read(image):
    """Read the scaling of the axis of the downloaded file. See `download()`.

    Parameters
    ----------
    image: cv2 image
        The input file

    Returns
    -------
    float
        scaling factor of y axis to pixels
    """
    print("")
    # Cut out the scale on the y-axis
    images = np.hstack([image[360:530, 1:55, :]])
    # Pick the grey scale
    images = images[:, :, 0]
    # Make it clearer, b/w, with threshold
    threshold = 150
    images[images < threshold] = 0
    images[images >= threshold] = 255
    # Read digits in image with tesseract
    data = pytesseract.image_to_boxes(
        images,
        lang="eng",
        config="--psm 6 digits --oem 3 -c tessedit_char_whitelist=0123456789",
    )

    # Extract scales from strings
    d = data.split("\n")
    d = [data for data in d if len(data) > 1]
    d = d[::-1]  # Reverse
    c = 0
    y_level = 0
    lim_0 = ""
    y_0 = ""
    lim_1 = ""
    y_1 = ""
    for ell in d:
        ell = ell.split()
        # if ell[0] != "-" and y_level != int(ell[2]):
        if y_level != int(ell[2]):
            y_level = int(ell[2])
            c += 1
            if c == 1:
                lim_0 += ell[0]
                y_0 = ell[2]
            elif c == 2:
                lim_1 += ell[0]
                y_1 = ell[2]
        elif y_level == int(ell[2]):
            if c == 1:
                lim_0 += ell[0]
                y_0 = ell[2]
            elif c == 2:
                lim_1 += ell[0]
                y_1 = ell[2]
        if c >= 3:
            break
    lim_0 = float(lim_0[::-1])
    y_b = float(y_0)
    lim_1 = float(lim_1[::-1])
    y_t = float(y_1)
    # Calculate the scale along the y-axis using the values and their position in the
    # image
    return 1 / round(abs(lim_1 - lim_0) / abs(y_t - y_b), 4)


def find_colour(image):
    """Find the pixels in an image with colour within a given range.

    Parameters
    ----------
    image: cv2 image
        The input file
    """
    # Define the list of boundaries
    boundaries = [
        # ([17, 15, 100], [50, 56, 200]),  # red
        ([86, 4, 4], [255, 100, 100])  # blue
        # ([25, 146, 190], [62, 174, 250]),  # yellow
        # ([103, 86, 65], [145, 133, 128])  # grey
    ]

    # Loop over the boundaries for (lower, upper) in boundaries:
    lower, upper = boundaries[0]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # Find the colours within the specified boundaries and apply
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
    cv2.imwrite("assets/new_im.jpg", np.hstack([output]))


def main():
    """Analyse image for a colour and return the scaling of the plot axis in the image.

    Returns
    -------
    scaling: float
        The scaling to make pixels and value axis in plot equal.
    """
    # Download image
    image = download()
    scaling = read(image)
    # Crop image
    y_h = int(image.shape[0] * 0.4)
    x_h = int(image.shape[1] * 0.1)
    image = np.hstack([image[y_h:, x_h:, :]])

    # Find colour of a given image and set to white,
    # the rest is set to black. Then save.
    find_colour(image)

    return scaling


if __name__ == "__main__":
    main()
