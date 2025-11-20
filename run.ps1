# CuraLink - Development Server Launcher
# Quick script to activate venv and run the server

Write-Host ""
Write-Host "Starting CuraLink Development Server..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Check if database exists
if (-not (Test-Path "db.sqlite3")) {
    Write-Host ""
    Write-Host "⚠ Database not found. Running migrations..." -ForegroundColor Yellow
    python manage.py migrate
    Write-Host ""
    $response = Read-Host "Do you want to populate sample data? (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        python manage.py populate_data
    }
}

Write-Host ""
Write-Host "=" * 61 -ForegroundColor Cyan
Write-Host "  CuraLink Server Starting..." -ForegroundColor Green
Write-Host "=" * 61 -ForegroundColor Cyan
Write-Host ""
Write-Host "  Homepage: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "  Admin:    http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "  API:      http://127.0.0.1:8000/api/" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run server
python manage.py runserver
