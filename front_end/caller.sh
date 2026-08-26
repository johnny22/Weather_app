#!/bin/bash
# this is for calling from cron
START=$SECONDS
cd /home/john/Weather_app/front_end
PATH=/usr/local/bin:$PATH
#/home/john/.local/bin/pipenv run python data_getter.py
uv run python data_getter.py
END=$SECONDS
DIFF=$(( $END - $START ))
echo "Total elapsed time was $DIFF"

