#!/bin/bash
set -e
python manage.py migrate --noinput
#python manage.py createsuperuser --noinput