#!/usr/bin/bash

export DJANGO_SETTINGS_MODULE=main.settings
celery -A main.celery worker --loglevel info --concurrency 5
