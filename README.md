# northern-lights-forecast
> A simple northern lights forecast that automatically send an email during substorm events.

### How?
This script implements an automated Northern Lights forecast by taking advantage of web scraping of the web site of the IMAGE Magnetometer.

At a given threshold of the derivative of the X component of a magnetometer in Tromsø, an email is sent to let the user know of a substorm event.

### crontab
The script can be run every hour from 18:00 through 04:00 during
the months September through March, using crontab to automate the task.
To edit the crontab script, type
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
