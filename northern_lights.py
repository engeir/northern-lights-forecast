#!/usr/bin/python3
"""This script implements an automated Northern Lights forecast
by taking advantage of web scraping of the web site of the IMAGE Magnetometer.
At a given threshold of the derivative of the X component,
an email is sent to let the user know a substorm has sparked.

The script is run every hour from 18:00 through 04:00 during
the months September through March, using crontab to automate the task.
To edit the crontab script, type
```
    env EDITOR=nano crontab -e
```
into the terminal.
"""

import smtplib
import numpy as np

from browser import open_browser
import img
import image_analysis as ima


def create_file():
    with open('user.py', 'w') as file:
        f_e = str(input('Type in the address of the email you want to send from:\t'))
        f_p = str(input('Type in the password of the email you want to send from:\t'))
        t_e = str(input('Type in the address of the email you want to send to:\t'))
        file.write(f'FROM_EMAIL = "{f_e}"\n')
        file.write(f'FROM_PASSWORD = "{f_p}"\n')
        file.write(f'TO_EMAIL = "{t_e}"\n')


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


try:
    import user
except Exception:
    create_file()
finally:
    import user

# Set which method to use.
# version = 'selenium_scrape'
version = 'img_analysis'

if version == 'selenium_scrape':
    dy = open_browser(hide=True)
    if dy < - 10:
        send_email(f'Northern Lights Warning!\n\nGradient: {np.min(dy)}\n\nHave a look at: http://fox.phys.uit.no/ASC/ASC01.html')
elif version == 'img_analysis':
    scaling = img.main()
    dy = ima.main(scaling)
    if dy < - 2:
        send_email(f'Northern Lights Warning!\n\nGradient: {np.min(dy)}\n\nHave a look at: http://fox.phys.uit.no/ASC/ASC01.html')
