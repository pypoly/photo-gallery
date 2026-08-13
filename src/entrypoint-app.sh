#!/usr/bin/bash

export DJANGO_SETTINGS_MODULE=main.settings
python manage.py migrate
gunicorn main.wsgi:application --bind 0.0.0.0:8000