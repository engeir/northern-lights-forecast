"""Test cases for the image_analysis module."""
import numpy as np
import pytest

from northern_lights_forecast import image_analysis


def test_mean_x() -> None:
    """Test that calculating mean along x-axis works."""
    x = np.array([1, 2, 2, 2, 3, 4, 5, 5])
    y = np.array([20, 16, 17, 18, 14, 10, 12, 14])
    x_, y_ = image_analysis.mean_x(x, y)
    assert np.array_equal(x_, np.array([1, 2, 3, 4, 5]))
    assert np.array_equal(y_, np.array([20, 17, 14, 10, 13]))

    y = y[:-1]
    with pytest.raises(ValueError):
        _, _ = image_analysis.mean_x(x, y)


def test_removel_line() -> None:
    """Test that lines along x-axis are removed correctly."""
    # The remove_lien function should remove the values from two arrays, x and y, that
    # correspond to the highest number of equal y-values.
    x = np.arange(1000)
    y = np.arange(1000) - 500
    # In this case, the zero-line is the second most numerous, but should still be removed
    y[:110] = 1
    y[300:450] = 2
    y[600:705] = 0
    # y = 9999, however, should be kept
    y[800:890] = 9999
    x_, y_ = image_analysis.remove_line(x, y)
    assert len(x_) == 632, f"Actually, x_.shape = {x_.shape}"
    assert x_.shape == y_.shape, "Shapes of output arrays do not match"
    assert (y_ == 9999).sum() == 90, f"Actually, 9999 is found {(y_==9999).sum()} times"


# Create plot of simple data in a mock file system, load into the function and compare
# the new plot with the original.
def test_grab_blue_line() -> None:
    """Test that we are able to obtain line in plot."""
    im = fake_image()
    scale1 = 1
    scale2 = 10
    gradient1 = image_analysis.grab_blue_line(scale1, im)
    gradient2 = image_analysis.grab_blue_line(scale2, im)
    assert abs(10 * gradient1 - gradient2) < 1e-10


def fake_image() -> np.ndarray:
    """Create mock image for test cases."""
    im = np.zeros((100, 100, 3))
    for i in range(50):
        im[-1 - i, i, 2] = 255
        im[-1 - i, 99 - i, 2] = 255
    im[80, :, 2] = 255
    return im


if __name__ == "__main__":
    im = fake_image()
    gradient1 = image_analysis.grab_blue_line(1, im)
    test_grab_blue_line()
