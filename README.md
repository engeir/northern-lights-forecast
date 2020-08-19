# northern-lights-forecast
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
The script can be run every hour from 18:00 through 04:00 during the months September through March, using crontab to automate the task. To edit the crontab script, type
```
env EDITOR=nano crontab -e
```
into the terminal.

Enter
```
0 0-4,18-23 * 9-12,1-3 * export DISPLAY=:0 && cd /path/to/folder/containing/script && python northern_lights.py >> t.txt 2>&1
```
to set the script to run as described above, or edit to a custom setting:
https://crontab.guru/
