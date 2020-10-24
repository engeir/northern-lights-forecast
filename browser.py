import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import numpy as np


def open_browser(hide=True):
    try:
        if hide:
            opts = Options()
            opts.headless = True
            browser = webdriver.Firefox(options=opts)
        else:
            browser = webdriver.Firefox()

        dy = navigate(browser)
    finally:
        try:
            browser.quit()
        except:
            pass

    return dy


def navigate(browser):
    browser.get('https://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=tro2a&year=2020&month=1&day=1&res=1min&pwd=&format=html&comps=DHZ&RTData=+Get+Realtime+Data+')
    time.sleep(5)

    pure = browser.find_element_by_xpath('/html/body/pre')
    saved = pure.text.splitlines()
    for v, ss in enumerate(saved):
        saved[v] = ss.split()

    del saved[0]
    del saved[0]
    del saved[0]
    del saved[0]
    del saved[0]
    del saved[0]
    s = np.array(saved)
    s = s[-120:, 3]  # Chose the last 2 hours (120 mins)
    y = s.astype(np.float)
    y = np.asarray([v for v in y if v % 99999.9])
    dy = np.gradient(y)

    return np.min(dy)
