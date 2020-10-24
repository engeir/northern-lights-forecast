# Northern Lights Forecast
![CodeQL](https://github.com/engeir/northern-lights-forecast/workflows/CodeQL/badge.svg)
> A simple web scraping northern lights forecast that automatically send an email during substorm events

## Use
Run the script once to input an email address to send from, including password, and the email you want to receive the notification. Alternatively, create a file called `user.py` and paste in
```
FROM_EMAIL = "from_email@gmail.com"
FROM_PASSWORD = "password"
TO_EMAIL = "to_email@gmail.com"
```
with the correct email addresses and password.

To be able to receive email notification, an email that the script can send from must be added. Follow [this](https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development) description to get started.

## How?
The script implements an automated Northern Lights forecast by taking advantage of the web site of [Tromsø Geophysical Observatory](http://geo.phys.uit.no/) (TGO). Two methods was created to be able to consistently obtain needed data.

### 1: Image analysis
The script will try to download a [`.gif`](https://flux.phys.uit.no/Last24/Last24_tro2a.gif) file with plots of the components of a magnetometer. One component is all that is needed (blue line) and the script will then locate the blue pixels and fit a graph to the pixel locations with a [Savitzky-Golay filter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html).
![]()
![]()

### 2: Web scraping
The script will do web scraping of the web site of [TGO](http://geo.phys.uit.no/) and download the raw data that is used to create [this](https://flux.phys.uit.no/Last24/Last24_tro2a.gif) plot.

### Finally
At a given threshold of the derivative of the X component of a magnetometer in Tromsø, an email is sent to let the user know of the current substorm event.

## cron
> Tested with macOS and Ubuntu

The script can be run every hour from 18:00 through 04:00 during the months September through March, using cron to automate the task. Run
```
bash crontab.sh <username>
```
(might need `sudo bash crontab.sh <username>`) to set this up (change to your own user name), or edit the cron script manually with
```
env EDITOR=nano crontab -e
```
Add
```
0 0-4,18-23 * 9-12,1-3 * export DISPLAY=:0 && cd /path/to/folder/containing/script && python3 northern_lights.py >> t.txt 2>&1
```
to the script to set cron to run as described above, or edit to a custom setting:
https://crontab.guru/

## Issues
### Geckodriver
If Geckodriver is not in `PATH` see [https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path](https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path).

### Crontab
If you get the error `no crontab for <usename>`, do
```
crontab -e
```
and choose which ever version you prefer.

Python, Geckodriver and Pytesseract need to be specified in `PATH` for cron to work. I.e. if Python sits at `/usr/bin`, Geckodriver at `/home/<username>` and Pytesseract at `/usr/local/bin`, do
```
crontab -u <username> -e
```
and add
```
PATH=/home/<username>:/usr/bin:/usr/local/bin
```
to the first line.
