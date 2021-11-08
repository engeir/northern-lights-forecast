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

# now, $1=="git", $2=="pull"

# username=$(whoami)
PWD=$(pwd)
exe=$(python -c "import sys;print(sys.executable)")
line="0 0-4,18-23 * 9-12,1-3 * export DISPLAY=:0 && cd $PWD && $exe src/northern_lights_forecast/__main__.py >> t.txt 2>&1"
if $has_p_option; then
    echo "$line"
else
    (crontab -l; echo "$line" ) | crontab -
    # (crontab -u "$username" -l; echo "$line" ) | crontab -u "$username" -
fi
