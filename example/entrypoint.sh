#!/usr/bin/env bash
python manage.py migrate --noinput

python manage.py loaddata fixtures.json 

echo "Starting server..."
gunicorn tickets.wsgi -b 0.0.0.0:8088 -w 2
