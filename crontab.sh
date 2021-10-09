#!/bin/bash
username=$(whoami)
PWD=$(pwd)
exe=$(python -c "import sys;print(sys.executable)")
line="0 0-4,18-23 * 9-12,1-3 * export DISPLAY=:0 && cd "$PWD" && $exe src/northern_lights_forecast/__main__.py >> t.txt 2>&1"
(crontab -u "$username" -l; echo "$line" ) | crontab -u "$username" -
