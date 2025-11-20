#!/bin/bash
# CuraLink Setup Script for macOS/Linux
# This script will set up the complete CuraLink application

echo "=============================================================="
echo "  CuraLink - Your Bridge to Better Health"
echo "  Automated Setup Script"
echo "=============================================================="
echo ""

# Check if Python is installed
echo "[1/8] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "  ✓ $PYTHON_VERSION found"
else
    echo "  ✗ Python not found. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment
echo ""
echo "[2/8] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "  ! Virtual environment already exists"
else
    python3 -m venv venv
    echo "  ✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "[3/8] Activating virtual environment..."
source venv/bin/activate
echo "  ✓ Virtual environment activated"

# Install dependencies
echo ""
echo "[4/8] Installing dependencies..."
pip install -r requirements.txt --quiet
echo "  ✓ Dependencies installed"

# Run migrations
echo ""
echo "[5/8] Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo "  ✓ Database migrations completed"

# Create superuser prompt
echo ""
echo "[6/8] Creating superuser (admin account)..."
echo "  Please enter admin credentials:"
python manage.py createsuperuser

# Populate sample data
echo ""
echo "[7/8] Populating sample data..."
read -p "  Do you want to populate sample data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py populate_data
    echo "  ✓ Sample data populated"
else
    echo "  ⊘ Skipped sample data population"
fi

# Setup complete
echo ""
echo "[8/8] Setup complete!"
echo ""
echo "=============================================================="
echo "  Setup Successfully Completed!"
echo "=============================================================="
echo ""
echo "Sample Test Credentials:"
echo "  Patient - username: patient1, password: patient123"
echo "  Doctor  - username: doctor1, password: doctor123"
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://127.0.0.1:8000/"
echo ""
echo "Admin panel: http://127.0.0.1:8000/admin/"
echo "API documentation: http://127.0.0.1:8000/api/"
echo ""
