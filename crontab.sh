#!/bin/bash
username=$1
PWD=$(pwd)
line="0 0-4,18-23 * 9-12,1-3 * export DISPLAY=:0 && cd "$PWD" && python3 im_to_plt.py >> t.txt 2>&1"
(crontab -u "$username" -l; echo "$line" ) | crontab -u "$username" -
