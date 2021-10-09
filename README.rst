Northern Lights Forecast
========================

|PyPI| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/northern-lights-forecast.svg
   :target: https://pypi.org/project/northern-lights-forecast/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/northern-lights-forecast
   :target: https://pypi.org/project/northern-lights-forecast
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/northern-lights-forecast
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/northern-lights-forecast/latest.svg?label=Read%20the%20Docs
   :target: https://northern-lights-forecast.readthedocs.io/
   :alt: Read the documentation at https://northern-lights-forecast.readthedocs.io/
.. |Tests| image:: https://github.com/engeir/northern-lights-forecast/workflows/Tests/badge.svg
   :target: https://github.com/engeir/northern-lights-forecast/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/engeir/northern-lights-forecast/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/engeir/northern-lights-forecast
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


* Send alerts using something else than email (telegram?)
  Follow:

Features
--------

Get notified whenever there are good chances of seeing northern lights! Follow
`@NorthernLightsForecastBot` on telegram for updates on the Tromsø magnetometer, or set up
your own telegram bot with this project. Setting up a telegram bot is easy as pie, just
follow `this guide`_.

Requirements
------------

The project uses `tesseract` to read off the scale on the magnetogram plots. See
installation instructions below.

Installation
------------

.. You can install *Northern Lights Forecast* via pip_ from PyPI_:

.. .. code:: console

..    $ pip install northern-lights-forecast

* Clone: `git clone https://github.com/engeir/northern-lights-forecast.git nlf && cd nlf`
* Install tesseract_, used with the package pytesseract.
* The get yourself a telegram bot using `this guide`_.
* Set up a virtual environment and activate. (Use whatever, for example poetry: `poetry
  shell`)
* Now we are ready to install the project; run `poetry install` in the root of the project
* Set up a cron job: `sh crontab.sh`.

Usage
-----

Please see the `Command-line Reference <Usage_>`_ for details.

How?
----

The script implements an automated Northern Lights forecast by taking advantage of the web
site of `Tromsø Geophysical Observatory`_ (TGO).

Image analysis
^^^^^^^^^^^^^^

The script will try to download a :code:`.gif` file with plots of the components of a
magnetometer. One component is all that is needed (blue line) and the script will then
locate the blue pixels and fit a graph to the pixel locations with a `Savitzky-Golay
filter`_.

Below is an example with the original image above the new reverse engineered graph.

.. image:: assets/before.jpg

.. image:: assets/after.png

At a given threshold of the derivative of the X component of a magnetometer in Tromsø, a
notification is sent to a telegram bot to let the user know of the current substorm event.

Cron
----

The script can be run every hour from 18:00 through 04:00 during the months September
through March, using cron to automate the task. Run

.. code:: console

    bash crontab.sh

to set this up, or edit the cron script manually with

.. code:: console

    env EDITOR=nano crontab -e

and add

.. code:: console

    0 0-4,18-23 * 9-12,1-3 * export DISPLAY=:0 && cd /path/to/folder/containing/script && python northern_lights.py >> t.txt 2>&1

to the script to set cron to run as described above, or edit to a custom
setting: https://crontab.guru/

When setting up cron, the python environment and the tesseract executable has
to be included to path in the cron script. If the older version using selenium
is used then geckodriver is needed in path.

Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*Northern Lights Forecast* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/engeir/northern-lights-forecast/issues
.. _pip: https://pip.pypa.io/
.. _tesseract: https://tesseract-ocr.github.io/tessdoc/Compiling-%E2%80%93-GitInstallation.html
.. _RealPython: https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
.. _Tromsø Geophysical Observatory: https://www.tgo.uit.no/
.. _this guide: https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580
.. _Savitzky-Golay filter: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://northern-lights-forecast.readthedocs.io/en/latest/usage.html
