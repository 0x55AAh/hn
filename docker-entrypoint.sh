#!/usr/bin/env bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Create django superuser
#echo "Creating django superuser"
#python manage.py createsuperuser

# Run hn startparser script
#echo "Run startparser"
#python manage.py startparser

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000