"""Scrape the website of TGO for magnetometer data using the selenium module."""
import time

import numpy as np
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def open_browser(hide: bool = True):
    """Handle open of browser with a try statement in case of failure.

    Parameters
    ----------
    hide: bool
        Toggle headless browser, True give headless.

    Returns
    -------
    dy: float
        The gradient returned by navigate()
    """
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
        except Exception:
            print("No open browsers to quit.")

    return dy


def navigate(browser) -> float:
    """Navigate the TGO website.

    Get the contents of the magnetometer data an analyse for a large,
    negative gradient.

    Parameters
    ----------
    browser: selenium.webdriver
        A webdriver object, e.g. selenium.webdriver.Firefox()

    Returns
    -------
    float
        The gradient returned by navigate()
    """
    # # With the requests module
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) \
    # Gecko/20100101 Firefox/7.0.1"
    # }
    # results = requests.get(
    #     "https://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=tro2a&year=2020&month" +
    #     "=1&day=1&res=1min&pwd=&format=html&comps=DHZ&RTData=+Get+Realtime+Data+"
    #     , headers=headers
    # )
    # # if check:
    # print([results.ok])
    # src = results.content
    # print(src)
    # soup = BeautifulSoup(src, "lxml")
    # txt = soup.find("a", class_="css-1ej4hfo").text.upper()

    # With the selenium module
    browser.get(
        "https://flux.phys.uit.no/cgi-bin/mkascii.cgi?site=tro2a&year=2020&"
        + "month=1&day=1&res=1min&pwd=&format=html&comps=DHZ&RTData=+Get+Realtime+Data+"
    )
    time.sleep(5)
    pure = browser.find_element_by_xpath("/html/body/pre")

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


if __name__ == "__main__":
    open_browser(hide=False)
