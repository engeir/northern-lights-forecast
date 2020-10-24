"""This script finds a white line and plots the line.
From https://stackoverflow.com/questions/60051941/find-the-coordinates-in-an-image-where-a-specified-colour-is-detected
"""

import smtplib
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# from northern_lights import send_email
import user

def send_email(txt):
    content = (str(txt))
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    # mail.login('eirik.r.enger.dev@gmail.com', 'ere_deveasypass')
    mail.login(f'{user.FROM_EMAIL}', f'{user.FROM_PASSWORD}')
    mail.sendmail(f'{user.FROM_EMAIL}',
                  f'{user.TO_EMAIL}', content)
    mail.close()


def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


def mean_x(x, y):
    idx = np.unique(x)
    x_ = np.array([])
    y_ = np.array([])
    for i in idx:
        x_ = np.r_[x_, np.mean(x[x==i])]
        y_ = np.r_[y_, np.mean(y[x==i])]
    return x_, y_


def remove_line(x, y):
    (values, counts) = np.unique(y, return_counts=True)
    values = values[np.argsort(counts)]
    counts = counts[np.argsort(counts)]
    idx = np.argwhere(counts > 100)
    val = values[idx]
    for v in val:
        x = x[y != v]
        y = y[y != v]
    return x, y


def find_gradient(x, y):
    pass

def main(scaling):
    # Load image
    im = cv2.imread('new_im.jpg')

    # Define the blue colour we want to find - remember OpenCV uses BGR ordering
    blue = [255, 255, 255]

    # Get X and Y coordinates of all blue pixels
    Y, X = np.where(np.all(im == blue, axis=2))

    x = X[np.argsort(X)]
    y = Y[np.argsort(X)]
    x, y = remove_line(x, y)
    y = scaling * y
    x_mean, y_mean = mean_x(x, y)
    x_ = np.linspace(np.min(x_mean), np.max(x_mean), 10000)
    y_i = - np.interp(x_, x_mean, y_mean)
    y_ = savgol_filter(y_i, 501, 3)  # window size 51, polynomial order 3
    dy = savgol_filter(y_i, 501, 3, deriv=1)  # window size 51, polynomial order 3
    if np.min(dy) < - 2:
        send_email(f'Northern Lights Warning!\n\nGradient: {np.min(dy)}')

    # Rescale x-axis to 22-hour plot
    # TODO: find the exact timespan used in the image
    # x = (x - np.min(x)) / (np.max(x) - np.min(x)) * 22
    # x_ = (x_ - np.min(x_)) / (np.max(x_) - np.min(x_)) * 22
    # plt.figure()
    # plt.plot(x, - y, 'b')
    # plt.plot(x_, y_, 'r')
    # plt.figure()
    # plt.plot(x_, dy, 'r')
    # plt.show()


if __name__ == '__main__':
    main(3)
