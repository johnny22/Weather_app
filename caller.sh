#!/bin/sh
# call this from cron to get the data and store it in the database
cd /home/john/Weather_app
PATH=/usr/local/bin:$PATH
#./home/john/.local/share/virtualenvs/Weaher_app-NA3VrAeW/bin/activate
#/home/john/.local/bin/pipenv run python run.py
pipenv run python run.py
./front_end/caller.sh

#python run.py
