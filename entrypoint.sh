#!/bin/sh
cd /app

echo
python manage.py wait_for_db

echo
python manage.py migrate --noinput
python manage.py collectstatic --noinput


echo
exec "$@"