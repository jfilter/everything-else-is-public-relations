#!/bin/bash
while ! nc -w 1 -z db 5432; do sleep 0.1; done;
/code/manage.py migrate;
/code/manage.py clean_db;
/code/manage.py run_huey --huey-verbose &
# /code/manage.py run_huey &
while :; do /code/manage.py runserver_plus 0.0.0.0:8000; sleep 1; done;
