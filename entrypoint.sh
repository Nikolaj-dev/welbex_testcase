#!/bin/sh

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Initialize the database
python delivery_app.init_db.py

# Start Celery worker
celery -A welbex.celery worker -l info -P threads &

# Start Celery beat
celery -A welbex beat -l info &

# Start Django server
exec "$@"
