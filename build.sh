#!/usr/bin/env bash
# Build script for CuraLink deployment
# This script is executed during the deployment process

set -o errexit  # Exit on error

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Creating superuser (if needed)..."
# Check if DJANGO_SUPERUSER_USERNAME is set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --no-input --email "${DJANGO_SUPERUSER_EMAIL:-admin@curalink.com}" || true
fi

echo "Importing hospital data..."
# Import hospital data only if not already imported
python manage.py import_hospitals || true

echo "Build completed successfully!"
