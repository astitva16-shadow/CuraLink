# CuraLink Setup Script for Windows PowerShell
# This script will set up the complete CuraLink application

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "  CuraLink - Your Bridge to Better Health" -ForegroundColor Green
Write-Host "  Automated Setup Script" -ForegroundColor Green
Write-Host "=" * 61 -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/8] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "[2/8] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ! Virtual environment already exists" -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[3/8] Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "[4/8] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "  ✓ Dependencies installed" -ForegroundColor Green

# Run migrations
Write-Host ""
Write-Host "[5/8] Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations --noinput
python manage.py migrate --noinput
Write-Host "  ✓ Database migrations completed" -ForegroundColor Green

# Create superuser prompt
Write-Host ""
Write-Host "[6/8] Creating superuser (admin account)..." -ForegroundColor Yellow
Write-Host "  Please enter admin credentials:" -ForegroundColor Cyan
python manage.py createsuperuser

# Populate sample data
Write-Host ""
Write-Host "[7/8] Populating sample data..." -ForegroundColor Yellow
$response = Read-Host "  Do you want to populate sample data? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    python manage.py populate_data
    Write-Host "  ✓ Sample data populated" -ForegroundColor Green
} else {
    Write-Host "  ⊘ Skipped sample data population" -ForegroundColor Yellow
}

# Setup complete
Write-Host ""
Write-Host "[8/8] Setup complete!" -ForegroundColor Yellow
Write-Host ""
Write-Host "=" * 61 -ForegroundColor Cyan
Write-Host "  Setup Successfully Completed!" -ForegroundColor Green
Write-Host "=" * 61 -ForegroundColor Cyan
Write-Host ""
Write-Host "Sample Test Credentials:" -ForegroundColor Cyan
Write-Host "  Patient - username: patient1, password: patient123" -ForegroundColor White
Write-Host "  Doctor  - username: doctor1, password: doctor123" -ForegroundColor White
Write-Host ""
Write-Host "To start the development server, run:" -ForegroundColor Cyan
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Then visit: http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host ""
Write-Host "Admin panel: http://127.0.0.1:8000/admin/" -ForegroundColor Green
Write-Host "API documentation: http://127.0.0.1:8000/api/" -ForegroundColor Green
Write-Host ""
