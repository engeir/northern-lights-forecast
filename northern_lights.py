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
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import numpy as np


def create_file():
    with open('user.py', 'w') as file:
        f_e = str(input('Type in the adress of the email you want to send from:\t'))
        f_p = str(input('Type in the password of the email you want to send from:\t'))
        t_e = str(input('Type in the adress of the email you want to send to:\t'))
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


def open_browser(hide=True):
    try:
        if hide:
            opts = Options()
            opts.headless = True
            browser = webdriver.Firefox(options=opts)
        else:
            browser = webdriver.Firefox()

        navigate(browser)
    finally:
        try:
            browser.quit()
        except:
            pass


def navigate(browser):
    browser.get('https://space.fmi.fi/image/www/index.php?page=user_defined')
    time.sleep(5)

    clear = browser.find_element_by_css_selector('#clear_all')
    clear.click()

    time.sleep(1)
    tro = browser.find_element_by_css_selector('#TRO')
    tro.click()

    day = browser.find_element_by_css_selector(
        '#LengthDayMenu > option:nth-child(1)')
    day.click()
    hour = browser.find_element_by_css_selector(
        '#LengthHourMenu > option:nth-child(4)')
    hour.click()
    scale_100 = browser.find_element_by_css_selector(
        '#scaling > option:nth-child(2)')
    scale_100.click()
    submit = browser.find_element_by_css_selector('#submit_grams')
    submit.click()

    time.sleep(5)
    x_txt = browser.find_element_by_css_selector(
        '#download_links > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > a:nth-child(1)')
    x_txt.click()

    time.sleep(5)
    browser.switch_to.window(browser.window_handles[-1])

    time.sleep(1)
    pure = browser.find_element_by_xpath('/html/body/pre')
    saved = pure.text.splitlines()
    for v, ss in enumerate(saved):
        saved[v] = ss.split(' ')

    del saved[0]
    del saved[0]
    s = np.array(saved)
    s = s[:, 9]
    y = s.astype(np.float)
    dy = np.gradient(y)
    if np.min(dy) < - 20:
        send_email(f'Northern Lights Warning!\n\nGradient: {np.min(dy)}')


try:
    import user
except Exception:
    create_file()
finally:
    import user

open_browser(hide=True)
