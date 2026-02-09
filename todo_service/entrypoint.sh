#!/bin/sh

python3 manage.py migrate --fake sessions zero
python3 manage.py showmigrations
python3 manage.py migrate --fake-initial
python3 manage.py collectstatic --noinput
python3 manage.py create_admin
gunicorn config.wsgi:application --bind 0.0.0.0:${TODO_GUVICORN_PORT} --workers 4 --keep-alive 5 --max-requests 1000 --timeout 300 --worker-connections 2000 --graceful-timeout 30