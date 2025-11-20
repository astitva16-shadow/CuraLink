"""
Basic tests for CuraLink models
Run with: python manage.py test
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Patient, Doctor
from hospitals.models import Hospital
from appointments.models import Appointment
from datetime import date, time, timedelta

User = get_user_model()


class UserModelTest(TestCase):
    """Test User model"""
    
    def test_create_patient_user(self):
        """Test creating a patient user"""
        user = User.objects.create_user(
            username='testpatient',
            email='patient@test.com',
            password='testpass123',
            role='patient'
        )
        self.assertEqual(user.username, 'testpatient')
        self.assertEqual(user.role, 'patient')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_create_doctor_user(self):
        """Test creating a doctor user"""
        user = User.objects.create_user(
            username='testdoctor',
            email='doctor@test.com',
            password='testpass123',
            role='doctor'
        )
        self.assertEqual(user.username, 'testdoctor')
        self.assertEqual(user.role, 'doctor')


class PatientModelTest(TestCase):
    """Test Patient model"""
    
    def test_create_patient_profile(self):
        """Test creating a patient profile"""
        user = User.objects.create_user(
            username='patient1',
            email='patient1@test.com',
            password='testpass123',
            role='patient'
        )
        patient = Patient.objects.create(
            user=user,
            age=30,
            gender='M',
            address='Test Address'
        )
        self.assertEqual(patient.user.username, 'patient1')
        self.assertEqual(patient.age, 30)
        self.assertEqual(patient.gender, 'M')


class DoctorModelTest(TestCase):
    """Test Doctor model"""
    
    def test_create_doctor_profile(self):
        """Test creating a doctor profile"""
        user = User.objects.create_user(
            username='doctor1',
            email='doctor1@test.com',
            password='testpass123',
            role='doctor'
        )
        doctor = Doctor.objects.create(
            user=user,
            specialization='general',
            qualification='MBBS',
            experience_years=5,
            clinic_hospital='Test Hospital',
            consultation_fee=500
        )
        self.assertEqual(doctor.user.username, 'doctor1')
        self.assertEqual(doctor.specialization, 'general')
        self.assertEqual(doctor.experience_years, 5)


class HospitalModelTest(TestCase):
    """Test Hospital model"""
    
    def test_create_hospital(self):
        """Test creating a hospital"""
        hospital = Hospital.objects.create(
            name='Test Hospital',
            address='123 Test Street',
            city='Mumbai',
            contact_number='1234567890',
            has_emergency=True
        )
        self.assertEqual(hospital.name, 'Test Hospital')
        self.assertEqual(hospital.city, 'Mumbai')
        self.assertTrue(hospital.has_emergency)


class AppointmentModelTest(TestCase):
    """Test Appointment model"""
    
    def setUp(self):
        """Set up test data"""
        # Create patient
        patient_user = User.objects.create_user(
            username='patient',
            email='patient@test.com',
            password='testpass123',
            role='patient'
        )
        
        # Create doctor
        doctor_user = User.objects.create_user(
            username='doctor',
            email='doctor@test.com',
            password='testpass123',
            role='doctor'
        )
        self.doctor = Doctor.objects.create(
            user=doctor_user,
            specialization='general',
            qualification='MBBS',
            experience_years=5,
            clinic_hospital='Test Hospital',
            consultation_fee=500
        )
        
        self.patient_user = patient_user
    
    def test_create_appointment(self):
        """Test creating an appointment"""
        appointment_date = date.today() + timedelta(days=1)
        appointment = Appointment.objects.create(
            patient=self.patient_user,
            doctor=self.doctor,
            appointment_date=appointment_date,
            appointment_time=time(10, 0),
            symptoms='Test symptoms',
            status='pending'
        )
        self.assertEqual(appointment.patient.username, 'patient')
        self.assertEqual(appointment.doctor.user.username, 'doctor')
        self.assertEqual(appointment.status, 'pending')
