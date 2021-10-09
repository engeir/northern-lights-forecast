"""Check the web for signs of northern lights.

This script implements an automated Northern Lights forecast
by taking advantage of web scraping of the web site of the IMAGE Magnetometer.
At a given threshold of the derivative of the X component,
a notification is sent to let the user know a substorm has occurred.

The script is run every hour from 18:00 through 04:00 during
the months September through March, using crontab to automate the task.
To edit the crontab script, type
```sh
env EDITOR=nano crontab -e
```
into the terminal.
"""
import numpy as np
import telegram_send

import northern_lights_forecast.image_analysis as ima
import northern_lights_forecast.img as img


def telegram_test() -> None:
    """Test to see if you are able to send with telegram."""
    telegram_send.send(messages=["Test"])


def nlf(location: str) -> None:
    """Run the Northern Lights Forecast."""
    scaling = img.img_analysis(location)
    dy = ima.grab_blue_line(scaling)
    print(dy)
    if dy < -2:
        txt = (
            f"Northern Lights Warning!\n\nGradient: {np.min(dy)}\n\n"
            + "Have a look at: http://fox.phys.uit.no/ASC/ASC01.html"
        )
        telegram_send.send(messages=[txt])


def main() -> None:
    """Run 'northern_lights.py'."""
    nlf("Tromsø")


if __name__ == "__main__":
    main()
