# Northern Lights Forecast
![CodeQL](https://github.com/engeir/northern-lights-forecast/workflows/CodeQL/badge.svg)
> A simple web scraping northern lights forecast that automatically send an email during substorm events

### Use
Run the script once to input an email address to send from, including password, and the email you want to receive the notification. Alternatively, create a file called `user.py` and paste in
```
FROM_EMAIL = "from_email@gmail.com"
FROM_PASSWORD = "password"
TO_EMAIL = "to_email@gmail.com"
```
with the correct email addresses and password.

To be able to receive email notification, an email that the script can send from must be added. Follow [this](https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development) description to get started.

### How?
The script implements an automated Northern Lights forecast by taking advantage of web scraping of the web site of the IMAGE Magnetometer.

At a given threshold of the derivative of the X component of a magnetometer in Tromsø, an email is sent to let the user know of the current substorm event.

### crontab
> Works with macOS

The script can be run every hour from 18:00 through 04:00 during the months September through March, using crontab to automate the task. Run
```
bash crontab.sh username
```
(might need `sudo bash crontab.sh username`) to set this up (change to your own user name), or edit the crontab script manually with
```
env EDITOR=nano crontab -e
```
Add
```
0 0-4,18-23 * 9-12,1-3 * export DISPLAY=:0 && cd /path/to/folder/containing/script && python3 northern_lights.py >> t.txt 2>&1
```
to the script to set crontab to run as described above, or edit to a custom setting:
https://crontab.guru/


### Issues
##### Geckodriver
If Geckodriver is not in path see [https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path](https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path).

##### Crontab
If you get the error `no crontab for <usename>`, do
```
crontab -e
```
and choose which ever version you prefer.

Python and Geckodriver need to be specified in `PATH` for crontab to work. I.e. if Python sits at `/usr/bin` and Geckodriver is in `/home/<username>`, do
```
crontab -u <username> -e
```
and add
```
PATH=/home/<username>:/usr/bin
```
to the first line.
