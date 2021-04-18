"""Check the web for signs of northern lights.

This script implements an automated Northern Lights forecast
by taking advantage of web scraping of the web site of the IMAGE Magnetometer.
At a given threshold of the derivative of the X component,
an email is sent to let the user know a substorm has sparked.

The script is run every hour from 18:00 through 04:00 during
the months September through March, using crontab to automate the task.
To edit the crontab script, type
```sh
env EDITOR=nano crontab -e
```
into the terminal.
"""
import smtplib

import numpy as np

import northern_lights_forecast.image_analysis as ima
import northern_lights_forecast.img as img
from northern_lights_forecast.browser import open_browser


def create_file():
    """Create a user file for sending emails."""
    with open("src/northern_lights_forecast/user.py", "w") as file:
        f_e = str(input("Type in the address of the email you want to send from:\t"))
        f_p = str(input("Type in the password of the email you want to send from:\t"))
        t_e = str(input("Type in the address of the email you want to send to:\t"))
        file.write(f'FROM_EMAIL = "{f_e}"\n')
        file.write(f'FROM_PASSWORD = "{f_p}"\n')
        file.write(f'TO_EMAIL = "{t_e}"\n')


def send_email(txt):
    """Send email to an address given in user.py.

    Args:
        txt: str
            The text you want to include in the email.
    """
    # TODO: check if [sendgrid](https://sendgrid.com/) or
    # [mailgun](https://www.mailgun.com/) are better to use.
    content = str(txt)
    mail = smtplib.SMTP("smtp.gmail.com", 587)
    mail.ehlo()
    mail.starttls()
    # mail.login('eirik.r.enger.dev@gmail.com', 'ere_deveasypass')
    mail.login(f"{user.FROM_EMAIL}", f"{user.FROM_PASSWORD}")
    mail.sendmail(f"{user.FROM_EMAIL}", f"{user.TO_EMAIL}", content)
    mail.close()


try:
    import northern_lights_forecast.user as user
except Exception:
    create_file()
finally:
    import northern_lights_forecast.user as user

# Set which method to use.
# version = 'selenium_scrape'
version = "img_analysis"

if version == "selenium_scrape":
    dy = open_browser(hide=True)
    if dy < -10:
        send_email(
            f"Northern Lights Warning!\n\nGradient: {np.min(dy)}\n\n"
            + "Have a look at: http://fox.phys.uit.no/ASC/ASC01.html"
        )
elif version == "img_analysis":
    scaling = img.main()
    dy = ima.main(scaling)
    if dy < -2:
        send_email(
            f"Northern Lights Warning!\n\nGradient: {np.min(dy)}\n\n"
            + "Have a look at: http://fox.phys.uit.no/ASC/ASC01.html"
        )
