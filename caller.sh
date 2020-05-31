#!/bin/sh
# call this from cron to get the data and store it in the database
cd /home/jbilbro/Weather_app
PATH=/usr/local/bin:$PATH
/home/jbilbro/.local/bin/pipenv run python run.py
