#!/bin/sh

set -eu
export PYTHONWARNINGS="ignore::SyntaxWarning"

echo "Migrating Database..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Starting granian..."
# Using the granian binary installed in the virtual environment
exec granian config.wsgi:application --host 0.0.0.0 --port 80 --interface wsgi --workers 2
