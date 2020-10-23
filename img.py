"""This script finds all pixels with colour within a range a colours them white, while all other is coloured black.
From https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
"""

# import the necessary packages
import argparse
import numpy as np
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="/Users/eirikenger/n_l")
args = vars(ap.parse_args())
# load the image
image = cv2.imread(args["image"])


# define the list of boundaries
boundaries = [
    # ([17, 15, 100], [50, 56, 200]),  # red
    ([86, 31, 4], [255, 100, 50])  # blue
    # ([25, 146, 190], [62, 174, 250]),  # yellow
    # ([103, 86, 65], [145, 133, 128])  # grey
]

# loop over the boundaries
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    # print(np.max(output))
    output[output > 0] = 255
    # show the images
    cv2.imwrite('new_im.jpg', np.hstack([output]))
    # cv2.imshow("images", np.hstack([image, output]))
    # cv2.waitKey(0)
