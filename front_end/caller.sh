#!/bin/sh
# this is for calling from cron
cd /home/john/Weather_app/front_end
PATH=/usr/local/bin:$PATH
#/home/john/.local/bin/pipenv run python data_getter.py
pipenv run python data_getter.py
