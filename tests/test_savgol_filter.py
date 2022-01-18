"""Test cases for the image_analysis module."""
import numpy as np
import scipy.signal as sg

import northern_lights_forecast.savgol.savitzky_golay as my_sg


def test_savgol_filter() -> None:
    """Test Savitzky Golay filter implementation against the one in scipy."""
    t = np.linspace(-4, 4, 500)
    y = np.exp(-(t ** 2)) + np.random.normal(0, 0.05, t.shape)
    y_my_sg = my_sg.savitzky_golay(y, 31, 4)
    y_sg = sg.savgol_filter(y, 31, 4)
    my_dy = my_sg.savitzky_golay(y, 31, 3, deriv=1)
    dy = sg.savgol_filter(y, 31, 3, deriv=1)
    # End effects are different in the two implementations, but we just want to see if
    # they produce similar results, not equivalent results. Relative difference of 1e-9 is
    # pretty darn close.
    assert np.allclose(y_my_sg[50:-50], y_sg[50:-50], 1e-9)
    assert np.allclose(my_dy[50:-50], dy[50:-50], 1e-9)


if __name__ == "__main__":
    test_savgol_filter()
