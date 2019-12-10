#!/bin/bash
if [ -z "${manage_py}" ]; then 
    manage_py=manage.py
fi 
python3 ${manage_py} loaddata discord_default_schedule.json