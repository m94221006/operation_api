#!/usr/bin/env bash

ls -al /app/backend/api_server/django_static/js


until cd /app/backend/api_server
do
    echo "Waiting for server volume..."
done

until ./manage.py migrate
do
    echo "Waiting for postgres ready..."
    sleep 2
done

./manage.py collectstatic

./manage.py makemigrations

gunicorn api_server.wsgi --bind 0.0.0.0:8080 --workers 4 --threads 4 
#./manage.py runserver 0.0.0.0:8000 # --settings=settings.dev_docker
