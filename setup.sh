#!/bin/bash

# Exit if any command fails
set -e

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Set up PostgreSQL database and user
echo "Creating PostgreSQL database and user..."
psql -U $POSTGRES_USER <<EOF
CREATE DATABASE $DATABASE_NAME;
CREATE ROLE $DATABASE_USER WITH LOGIN SUPERUSER PASSWORD '$DATABASE_PASSWORD';;
GRANT ALL PRIVILEGES ON DATABASE $DATABASE_NAME TO $POSTGRES_USER;
EOF

# Check if virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser and regular user
echo "Creating Django superuser and regular user..."
python manage.py shell <<EOF
from django.contrib.auth.models import User, Group

# Create Admin group if it doesn't exist
admin_group, created = Group.objects.get_or_create(name='Admin')

# Create superuser
if not User.objects.filter(username='$SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')

# Create a regular user and assign to Admin group
if not User.objects.filter(username='$REGULAR_USERNAME').exists():
    user = User.objects.create_user('$REGULAR_USERNAME', '$REGULAR_EMAIL', '$REGULAR_PASSWORD')
    user.groups.add(admin_group)
EOF

echo "Setup complete!"
