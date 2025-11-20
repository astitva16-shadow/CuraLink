# CuraLink - Your Bridge to Better Health

A comprehensive health consultation and appointment booking platform built with Django.

## 🌟 Features

### Core Features
- **User Authentication**: Separate registration and login for patients and doctors
- **Doctor Listings**: Browse doctors by specialization with ratings and availability
- **Appointment Booking**: Easy-to-use appointment booking system with date/time validation
- **Consultation Summaries**: Doctors can create detailed consultation summaries with prescriptions
- **Symptom Checker**: Rule-based AI symptom checker providing preliminary health guidance
- **Hospital Finder**: Search hospitals by city and emergency services
- **🌍 GPS-Based Nearby Hospitals**: Live location detection to find hospitals within 100 km radius
- **🗺️ Interactive Map View**: Leaflet.js powered map with live location tracking and hospital markers
- **Emergency Section**: Quick access to emergency numbers and hospitals with emergency care
- **REST API**: Full-featured JSON API for mobile app integration

### User Roles
- **Patients**: Book appointments, check symptoms, view consultation history
- **Doctors**: Manage appointments, create consultation summaries, update availability

## 🛠️ Tech Stack

- **Backend**: Python Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (easily switchable to PostgreSQL)
- **Frontend**: Django Templates with Bootstrap 5
- **Maps**: Leaflet.js with OpenStreetMap tiles
- **Icons**: Bootstrap Icons
- **PDF Generation**: ReportLab (for consultation summaries)

## 📋 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
cd CuraLink
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt)**:
  ```cmd
  venv\Scripts\activate.bat
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Run Migrations
```powershell
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```powershell
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

**Example credentials for testing:**
- Username: `admin`
- Email: `admin@curalink.com`
- Password: `admin123` (choose a strong password)

### Step 7: Load Sample Data (Optional)
```powershell
python manage.py loaddata sample_data.json
```

### Step 8: Run Development Server
```powershell
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 👥 Sample Test Accounts

After running the server, you can create test accounts through the registration page:

### Patient Account
- Navigate to: Register → Patient
- Fill in the form with test data

### Doctor Account
- Navigate to: Register → Doctor
- Fill in professional details

**Or use admin panel** (`http://127.0.0.1:8000/admin/`) to create users directly.

## 🗂️ Project Structure

```
CuraLink/
├── curalink/              # Main project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py
├── accounts/              # User authentication & profiles
│   ├── models.py          # User, Patient, Doctor models
│   ├── views.py           # Authentication views
│   ├── forms.py           # Registration forms
│   └── urls.py
├── appointments/          # Appointment management
│   ├── models.py          # Appointment, ConsultationSummary
│   ├── views.py           # Booking and management views
│   ├── forms.py           # Appointment forms
│   └── urls.py
├── hospitals/             # Hospital listings
│   ├── models.py          # Hospital model
│   ├── views.py           # Hospital search and emergency
│   └── urls.py
├── symptoms/              # Symptom checker
│   ├── symptom_checker.py # Rule-based symptom analysis
│   ├── views.py           # Symptom checker interface
│   └── urls.py
├── api/                   # REST API
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API ViewSets
│   └── urls.py
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Landing page
│   ├── accounts/          # Authentication templates
│   ├── appointments/      # Appointment templates
│   ├── hospitals/         # Hospital templates
│   └── symptoms/          # Symptom checker template
├── manage.py
└── requirements.txt
```

## 🔌 API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

### Doctors
- `GET /api/doctors/` - List all doctors
- `GET /api/doctors/?specialization=cardiology` - Filter by specialization
- `GET /api/doctors/{id}/` - Get doctor details

### Hospitals
- `GET /api/hospitals/` - List all hospitals
- `GET /api/hospitals/?city=Mumbai` - Filter by city
- `GET /api/hospitals/?emergency=true` - Filter emergency hospitals
- `GET /api/hospitals/{id}/` - Get hospital details
- `GET /hospitals/nearby/?lat=19.0760&lon=72.8777&radius=10` - Find nearby hospitals (GPS-based)

### Appointments (Requires Authentication)
- `GET /api/appointments/` - List user's appointments
- `POST /api/appointments/` - Create new appointment
- `GET /api/appointments/{id}/` - Get appointment details
- `POST /api/appointments/{id}/cancel/` - Cancel appointment
- `POST /api/appointments/{id}/update_status/` - Update status (doctors only)

### Consultation Summaries (Requires Authentication)
- `GET /api/consultation-summaries/` - List accessible summaries
- `GET /api/consultation-summaries/{id}/` - Get summary details

## 🧪 Testing the Application

### 1. As a Patient:
1. Register as a patient
2. Browse doctors by specialization
3. Book an appointment with a doctor
4. Use the symptom checker
5. Search for hospitals
6. View your appointments in "My Appointments"
7. View consultation summaries after doctor completes them

### 2. As a Doctor:
1. Register as a doctor
2. View your appointments in "My Appointments"
3. Confirm pending appointments
4. Create consultation summaries for completed appointments
5. Add prescriptions and care instructions

### 3. GPS-Based Hospital Finder:
1. Go to the Hospitals page
2. Click "Find Nearby Hospitals" button
3. Allow location access when prompted
4. View hospitals sorted by distance (within 10 km)
5. Get directions via Google Maps integration

### 4. Admin Panel:
1. Login at `/admin/`
2. Manage users, doctors, patients
3. Add hospitals with GPS coordinates
4. View all appointments

## 🚑 Emergency Features

- Quick access to emergency numbers (112, 108)
- List of hospitals with emergency services
- Basic first aid tips
- One-click calling feature

## 🎨 UI/UX Features

- **Responsive Design**: Works on mobile, tablet, and desktop
- **Modern UI**: Clean, health-oriented color scheme (blue, green, white)
- **Interactive Elements**: Modals, alerts, form validations
- **Intuitive Navigation**: Easy-to-use navbar with role-based links
- **Print-Friendly**: Consultation summaries can be printed

## 🔒 Security Features

- Password hashing with Django's built-in authentication
- CSRF protection
- Session-based authentication
- Role-based access control
- Form validation

## 🚀 Production Deployment Checklist

Before deploying to production:

1. **Security Settings**:
   - Change `SECRET_KEY` in `settings.py`
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`
   - Configure HTTPS

2. **Database**:
   - Switch to PostgreSQL for production
   - Set up database backups

3. **Static Files**:
   - Run `python manage.py collectstatic`
   - Configure static file serving (Nginx/Apache)

4. **Environment Variables**:
   - Use environment variables for sensitive data
   - Install `python-decouple` for configuration

5. **Email Configuration**:
   - Set up email backend for notifications
   - Configure SMTP settings

## 📝 License

This project is created for educational and portfolio purposes.

## 👨‍💻 Author

Built as a comprehensive Django full-stack demonstration project.

## 🤝 Contributing

This is a portfolio project, but suggestions and feedback are welcome!

## 📧 Support

For issues or questions, please use the GitHub issues section or contact through the repository.

---

## 🎯 Recent Features

### 🌍 GPS-Based Nearby Hospital Detection (NEW!)
- **Live Location Detection**: Uses browser's geolocation API to detect user's current location
- **Distance Calculation**: Haversine formula for accurate distance calculation (in km)
- **Smart Filtering**: Find hospitals within 10 km radius (configurable)
- **Sorted Results**: Hospitals displayed nearest first with distance badge
- **Google Maps Integration**: Direct directions to each hospital
- **Privacy-First**: Location not stored, used only for search

**See full documentation**: `GPS_FEATURE_GUIDE.md`

## 🎯 Future Enhancements

Potential features for future versions:
- Interactive map view with hospital markers
- Video consultation integration
- Payment gateway for consultation fees
- SMS/Email notifications
- Medical records upload
- Real-time bed availability
- Prescription management system
- Lab test booking
- Medicine delivery integration
- Multi-language support
- Mobile app (React Native/Flutter)

---

**CuraLink** - Connecting patients with quality healthcare. 🏥💙
