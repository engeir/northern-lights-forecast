#!/bin/sh
has_p_option=false
while getopts :p opt; do
    case $opt in
        p) has_p_option=true ;;
        :) echo "Missing argument for option -$OPTARG"; exit 1;;
       \?) echo "Unknown option -$OPTARG"; exit 1;;
    esac
done

# here's the key part: remove the parsed options from the positional params
shift $(( OPTIND - 1 ))

# username=$(whoami)
PWD=$(pwd)
exe=$(python -c "import sys;print(sys.executable)")
if ! command -v tesseract > /dev/null 2>&1
then
    newpath="# Tesseract was not found. Make sure it is installed and is in PATH."
else
    tesseract=$(dirname "$(which tesseract)")
    newpath="PATH=\$PATH:$tesseract"
fi
before="# >>> Added by nlf - Northern Lights Forecast >>>"
after="# <<< Added by nlf - Northern Lights Forecast <<<"
line="0 0-8,18-23 * 9-12,1-3 * export DISPLAY=:0 && cd $PWD && $exe src/northern_lights_forecast/__main__.py > t.txt 2>&1"
if $has_p_option; then
    echo "$before"
    echo "$newpath"
    echo "$line"
    echo "$after"
else
    (crontab -l; echo "$before" ) | crontab -
    (crontab -l; echo "$newpath" ) | crontab -
    (crontab -l; echo "$line" ) | crontab -
    (crontab -l; echo "$after" ) | crontab -
    # (crontab -u "$username" -l; echo "$line" ) | crontab -u "$username" -
fi
