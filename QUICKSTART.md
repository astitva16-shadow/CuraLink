# CuraLink - Quick Start Guide

## ⚡ Quick Setup (Windows)

### Option 1: Using Setup Script (Recommended)
```powershell
# Run the automated setup script
.\setup.ps1
```

### Option 2: Manual Setup
```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create admin account
python manage.py createsuperuser

# 6. Populate sample data (optional)
python manage.py populate_data

# 7. Start server
python manage.py runserver
```

## 🌐 Access the Application

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/

## 👥 Test Accounts

After running `populate_data` command:

### Patients
- **Username**: `patient1` | **Password**: `patient123`
- **Username**: `patient2` | **Password**: `patient123`
- **Username**: `patient3` | **Password**: `patient123`

### Doctors
- **Username**: `doctor1` | **Password**: `doctor123` (General Physician)
- **Username**: `doctor2` | **Password**: `doctor123` (Cardiologist)
- **Username**: `doctor3` | **Password**: `doctor123` (Dermatologist)
- **Username**: `doctor4` | **Password**: `doctor123` (Pediatrician)
- **Username**: `doctor5` | **Password**: `doctor123` (Orthopedic)

## 🧪 Testing Workflow

### As a Patient:
1. Login with `patient1`/`patient123`
2. Browse doctors at `/appointments/doctors/`
3. Book an appointment
4. Check symptoms at `/symptoms/`
5. View hospitals at `/hospitals/`
6. Check emergency services at `/hospitals/emergency/`

### As a Doctor:
1. Login with `doctor1`/`doctor123`
2. View appointments at `/appointments/my-appointments/`
3. Confirm pending appointments
4. Add consultation summary for completed appointments

## 📡 API Testing

### Using Browser
Visit: http://127.0.0.1:8000/api/

### Using curl (PowerShell)
```powershell
# Get all doctors
curl http://127.0.0.1:8000/api/doctors/

# Get doctors by specialization
curl http://127.0.0.1:8000/api/doctors/?specialization=cardiology

# Get all hospitals
curl http://127.0.0.1:8000/api/hospitals/

# Get emergency hospitals
curl "http://127.0.0.1:8000/api/hospitals/?emergency=true"
```

## 🎨 Key Features to Test

### 1. User Registration
- Patient Registration: `/register/patient/`
- Doctor Registration: `/register/doctor/`

### 2. Appointment System
- Browse Doctors: `/appointments/doctors/`
- Book Appointment: `/appointments/book/`
- View Appointments: `/appointments/my-appointments/`

### 3. Symptom Checker
- Access: `/symptoms/`
- Try different symptom categories
- View recommendations and care instructions

### 4. Hospital Finder
- Browse Hospitals: `/hospitals/`
- Filter by city
- Filter by emergency services

### 5. Emergency Page
- Access: `/hospitals/emergency/`
- View emergency numbers
- Find emergency hospitals

### 6. Consultation Summaries
- Doctor creates summary after appointment
- Patient views summary
- Print-friendly format available

## 🛠️ Admin Panel Features

Login at `/admin/` with superuser credentials:

- Manage users (patients and doctors)
- View all appointments
- Add/edit hospitals
- Manage consultation summaries

## 🔧 Troubleshooting

### Port Already in Use
```powershell
python manage.py runserver 8001
```

### Database Issues
```powershell
# Delete database and recreate
Remove-Item db.sqlite3
python manage.py migrate
python manage.py populate_data
```

### Virtual Environment Issues
```powershell
# Deactivate and reactivate
deactivate
venv\Scripts\Activate.ps1
```

## 📚 Project Structure Highlights

- **Models**: `accounts/models.py`, `appointments/models.py`, `hospitals/models.py`
- **Views**: Located in each app's `views.py`
- **Templates**: `templates/` directory with organized subdirectories
- **API**: `api/views.py` and `api/serializers.py`
- **Symptom Checker**: `symptoms/symptom_checker.py`

## 🚀 Next Steps

1. Explore the codebase
2. Test all features as both patient and doctor
3. Try the REST API endpoints
4. Customize templates and styling
5. Add more features as needed

## 💡 Tips

- Use Chrome DevTools to inspect responsive design
- Check Django Debug Toolbar for query optimization (if installed)
- Use the admin panel to quickly create test data
- Test form validations by entering invalid data

## 📞 Need Help?

Refer to the main README.md for detailed documentation.

---

**Happy Coding! 🏥💙**
