# CuraLink API Documentation

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
The API uses **session-based authentication**. You need to be logged in to access protected endpoints.

### Login
```http
POST /accounts/login/
Content-Type: application/x-www-form-urlencoded

username=patient1&password=patient123
```

## API Endpoints

---

### 1. Doctors API

#### List All Doctors
```http
GET /api/doctors/
```

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 2,
        "username": "doctor1",
        "email": "doctor1@curalink.com",
        "first_name": "Rajesh",
        "last_name": "Sharma",
        "role": "doctor",
        "phone": "9123456780"
      },
      "specialization": "general",
      "specialization_display": "General Physician",
      "qualification": "MBBS, MD",
      "experience_years": 10,
      "clinic_hospital": "Apollo Hospital, Mumbai",
      "consultation_fee": "500.00",
      "bio": "Experienced general physician...",
      "rating": "4.50",
      "is_available": true
    }
  ]
}
```

#### Filter Doctors by Specialization
```http
GET /api/doctors/?specialization=cardiology
```

**Available Specializations:**
- `general` - General Physician
- `cardiology` - Cardiologist
- `dermatology` - Dermatologist
- `pediatrics` - Pediatrician
- `orthopedics` - Orthopedic
- `neurology` - Neurologist
- `gynecology` - Gynecologist
- `psychiatry` - Psychiatrist
- `gastroenterology` - Gastroenterologist
- `ent` - ENT Specialist

#### Get Doctor Details
```http
GET /api/doctors/{id}/
```

**Response:**
```json
{
  "id": 1,
  "user": {
    "id": 2,
    "username": "doctor1",
    "email": "doctor1@curalink.com",
    "first_name": "Rajesh",
    "last_name": "Sharma",
    "role": "doctor",
    "phone": "9123456780"
  },
  "specialization": "general",
  "specialization_display": "General Physician",
  "qualification": "MBBS, MD",
  "experience_years": 10,
  "clinic_hospital": "Apollo Hospital, Mumbai",
  "consultation_fee": "500.00",
  "bio": "Experienced general physician with expertise...",
  "rating": "4.50",
  "is_available": true
}
```

---

### 2. Hospitals API

#### List All Hospitals
```http
GET /api/hospitals/
```

**Response:**
```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Apollo Hospital",
      "address": "Sahar Road, Andheri East",
      "city": "Mumbai",
      "state": "Maharashtra",
      "contact_number": "022-26834343",
      "email": "apollo.mumbai@apollo.com",
      "has_emergency": true,
      "has_ambulance": true,
      "beds_available": 50,
      "description": "",
      "website": "",
      "rating": "4.00"
    }
  ]
}
```

#### Filter Hospitals by City
```http
GET /api/hospitals/?city=Mumbai
```

#### Filter Emergency Hospitals
```http
GET /api/hospitals/?emergency=true
```

#### Search Hospitals
```http
GET /api/hospitals/?search=Apollo
```

#### Get Hospital Details
```http
GET /api/hospitals/{id}/
```

---

### 3. Appointments API (Protected)

🔒 **Requires Authentication**

#### List User's Appointments
```http
GET /api/appointments/
Authorization: Session
```

**Response (Patient):**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "patient": {
        "id": 1,
        "username": "patient1",
        "email": "patient1@curalink.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "patient",
        "phone": "9876543210"
      },
      "doctor": {
        "id": 1,
        "user": {
          "id": 2,
          "username": "doctor1",
          "first_name": "Rajesh",
          "last_name": "Sharma"
        },
        "specialization_display": "General Physician"
      },
      "appointment_date": "2024-12-01",
      "appointment_time": "10:00:00",
      "symptoms": "Fever and headache",
      "status": "pending",
      "status_display": "Pending",
      "notes": "",
      "created_at": "2024-11-21T10:30:00Z",
      "updated_at": "2024-11-21T10:30:00Z"
    }
  ]
}
```

#### Create New Appointment
```http
POST /api/appointments/
Authorization: Session
Content-Type: application/json

{
  "doctor_id": 1,
  "appointment_date": "2024-12-01",
  "appointment_time": "10:00:00",
  "symptoms": "Fever and headache for 2 days",
  "notes": "Need urgent consultation"
}
```

**Response:**
```json
{
  "id": 1,
  "doctor_id": 1,
  "appointment_date": "2024-12-01",
  "appointment_time": "10:00:00",
  "symptoms": "Fever and headache for 2 days",
  "status": "pending",
  "status_display": "Pending",
  "notes": "Need urgent consultation",
  "created_at": "2024-11-21T10:30:00Z"
}
```

**Validation Rules:**
- `appointment_date`: Cannot be in the past
- `appointment_time`: Cannot be in the past (if date is today)
- `symptoms`: Required field
- `doctor_id`: Must be valid and available

#### Get Appointment Details
```http
GET /api/appointments/{id}/
Authorization: Session
```

#### Update Appointment Status (Doctors Only)
```http
POST /api/appointments/{id}/update_status/
Authorization: Session
Content-Type: application/json

{
  "status": "confirmed"
}
```

**Valid Status Values:**
- `pending`
- `confirmed`
- `completed`
- `cancelled`

#### Cancel Appointment
```http
POST /api/appointments/{id}/cancel/
Authorization: Session
```

**Response:**
```json
{
  "status": "Appointment cancelled successfully."
}
```

---

### 4. Consultation Summaries API (Protected)

🔒 **Requires Authentication**

#### List Consultation Summaries
```http
GET /api/consultation-summaries/
Authorization: Session
```

**Response:**
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "appointment": {
        "id": 1,
        "patient": {...},
        "doctor": {...},
        "appointment_date": "2024-11-20",
        "status": "completed"
      },
      "diagnosis": "Viral fever",
      "prescribed_medicines": "Paracetamol 500mg - 3 times daily\nVitamin C - Once daily",
      "instructions": "Take medicines after meals\nDrink plenty of fluids\nRest for 3 days",
      "diet_recommendations": "Light food\nAvoid oily and spicy food",
      "follow_up_required": true,
      "follow_up_date": "2024-11-27",
      "created_at": "2024-11-20T15:30:00Z",
      "updated_at": "2024-11-20T15:30:00Z"
    }
  ]
}
```

#### Get Consultation Summary
```http
GET /api/consultation-summaries/{id}/
Authorization: Session
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data",
  "errors": {
    "appointment_date": ["Cannot book appointments in the past."]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Pagination

All list endpoints support pagination:

```http
GET /api/doctors/?page=2
```

**Response:**
```json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/doctors/?page=3",
  "previous": "http://127.0.0.1:8000/api/doctors/?page=1",
  "results": [...]
}
```

Default page size: **10 items per page**

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider adding:
- Django REST Framework throttling
- Redis-based rate limiting
- API key authentication

---

## CORS Configuration

CORS is enabled for all origins in development. For production:
1. Set specific allowed origins in `settings.py`
2. Configure `CORS_ALLOWED_ORIGINS`
3. Enable credentials if needed

---

## Testing the API

### Using curl (PowerShell)

**Get all doctors:**
```powershell
curl http://127.0.0.1:8000/api/doctors/
```

**Filter by specialization:**
```powershell
curl "http://127.0.0.1:8000/api/doctors/?specialization=cardiology"
```

**Create appointment (requires session):**
```powershell
# First login to get session
curl -X POST http://127.0.0.1:8000/accounts/login/ `
  -d "username=patient1&password=patient123" `
  -c cookies.txt

# Then make authenticated request
curl -X POST http://127.0.0.1:8000/api/appointments/ `
  -H "Content-Type: application/json" `
  -b cookies.txt `
  -d '{\"doctor_id\":1,\"appointment_date\":\"2024-12-01\",\"appointment_time\":\"10:00\",\"symptoms\":\"Test\"}'
```

### Using Postman

1. **Import Collection**: Create a new collection
2. **Set Base URL**: `http://127.0.0.1:8000/api/`
3. **Authentication**: Use "Session" or manually login first
4. **Headers**: Set `Content-Type: application/json` for POST/PUT

### Using Python requests

```python
import requests

# Base URL
base_url = 'http://127.0.0.1:8000/api/'

# Get all doctors
response = requests.get(f'{base_url}doctors/')
doctors = response.json()

# Filter doctors
response = requests.get(f'{base_url}doctors/', params={'specialization': 'cardiology'})

# Create session for authenticated requests
session = requests.Session()
session.post('http://127.0.0.1:8000/accounts/login/', 
             data={'username': 'patient1', 'password': 'patient123'})

# Create appointment
appointment_data = {
    'doctor_id': 1,
    'appointment_date': '2024-12-01',
    'appointment_time': '10:00:00',
    'symptoms': 'Fever and headache'
}
response = session.post(f'{base_url}appointments/', json=appointment_data)
```

---

## Best Practices

1. **Always validate input data** before making API calls
2. **Handle errors gracefully** with try-catch blocks
3. **Store tokens/sessions securely** (never in code)
4. **Use HTTPS in production**
5. **Implement proper error handling**
6. **Log API calls for debugging**
7. **Respect rate limits** (when implemented)

---

## Support

For API issues or questions:
- Check error responses for details
- Review Django logs: `python manage.py runserver` output
- Check database state: `python manage.py shell`

---

**CuraLink API v1.0** - Built with Django REST Framework 🏥💙
