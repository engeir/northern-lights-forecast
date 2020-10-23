"""This script finds a white line and plots the line.
From https://stackoverflow.com/questions/60051941/find-the-coordinates-in-an-image-where-a-specified-colour-is-detected
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image
im = cv2.imread('new_im.jpg')

# Define the blue colour we want to find - remember OpenCV uses BGR ordering
blue = [255, 255, 255]
# 35, 38, 219

# Get X and Y coordinates of all blue pixels
Y, X = np.where(np.all(im == blue, axis=2))

# print(X, Y)
x = X[np.argsort(X)]
y = - Y[np.argsort(X)]
plt.plot(x, y)
plt.show()
# cv2.imshow('image', im)
# cv2.waitKey(0)
# cv2.destoyAllWindows()
