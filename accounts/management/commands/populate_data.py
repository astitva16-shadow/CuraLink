"""
Management command to populate the database with sample data for testing.
Run with: python manage.py populate_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Patient, Doctor
from hospitals.models import Hospital
from appointments.models import Appointment
from datetime import date, time, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data population...')
        
        # Create sample patients
        self.create_patients()
        
        # Create sample doctors
        self.create_doctors()
        
        # Create sample hospitals
        self.create_hospitals()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))
        self.stdout.write('\nSample Credentials:')
        self.stdout.write('Patient - username: patient1, password: patient123')
        self.stdout.write('Doctor - username: doctor1, password: doctor123')

    def create_patients(self):
        self.stdout.write('Creating sample patients...')
        
        patients_data = [
            {
                'username': 'patient1',
                'email': 'patient1@curalink.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '9876543210',
                'age': 28,
                'gender': 'M',
                'address': '123 Main Street, Mumbai'
            },
            {
                'username': 'patient2',
                'email': 'patient2@curalink.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone': '9876543211',
                'age': 35,
                'gender': 'F',
                'address': '456 Park Avenue, Delhi'
            },
            {
                'username': 'patient3',
                'email': 'patient3@curalink.com',
                'first_name': 'Raj',
                'last_name': 'Kumar',
                'phone': '9876543212',
                'age': 42,
                'gender': 'M',
                'address': '789 Lake Road, Bangalore'
            }
        ]
        
        for data in patients_data:
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password='patient123',
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    phone=data['phone'],
                    role='patient'
                )
                Patient.objects.create(
                    user=user,
                    age=data['age'],
                    gender=data['gender'],
                    address=data['address']
                )
                self.stdout.write(f"  Created patient: {data['username']}")

    def create_doctors(self):
        self.stdout.write('Creating sample doctors...')
        
        doctors_data = [
            {
                'username': 'doctor1',
                'email': 'doctor1@curalink.com',
                'first_name': 'Rajesh',
                'last_name': 'Sharma',
                'phone': '9123456780',
                'specialization': 'general',
                'qualification': 'MBBS, MD',
                'experience_years': 10,
                'clinic_hospital': 'Apollo Hospital, Mumbai',
                'consultation_fee': 500,
                'bio': 'Experienced general physician with expertise in treating common ailments.'
            },
            {
                'username': 'doctor2',
                'email': 'doctor2@curalink.com',
                'first_name': 'Priya',
                'last_name': 'Verma',
                'phone': '9123456781',
                'specialization': 'cardiology',
                'qualification': 'MBBS, MD (Cardiology)',
                'experience_years': 15,
                'clinic_hospital': 'Fortis Hospital, Delhi',
                'consultation_fee': 1000,
                'bio': 'Specialist in cardiovascular diseases with 15 years of experience.'
            },
            {
                'username': 'doctor3',
                'email': 'doctor3@curalink.com',
                'first_name': 'Amit',
                'last_name': 'Patel',
                'phone': '9123456782',
                'specialization': 'dermatology',
                'qualification': 'MBBS, MD (Dermatology)',
                'experience_years': 8,
                'clinic_hospital': 'Max Hospital, Bangalore',
                'consultation_fee': 700,
                'bio': 'Expert in skin, hair, and cosmetic treatments.'
            },
            {
                'username': 'doctor4',
                'email': 'doctor4@curalink.com',
                'first_name': 'Sneha',
                'last_name': 'Reddy',
                'phone': '9123456783',
                'specialization': 'pediatrics',
                'qualification': 'MBBS, MD (Pediatrics)',
                'experience_years': 12,
                'clinic_hospital': 'Rainbow Children Hospital, Hyderabad',
                'consultation_fee': 600,
                'bio': 'Dedicated pediatrician focusing on child healthcare.'
            },
            {
                'username': 'doctor5',
                'email': 'doctor5@curalink.com',
                'first_name': 'Vikram',
                'last_name': 'Singh',
                'phone': '9123456784',
                'specialization': 'orthopedics',
                'qualification': 'MBBS, MS (Orthopedics)',
                'experience_years': 18,
                'clinic_hospital': 'AIIMS, Delhi',
                'consultation_fee': 900,
                'bio': 'Specialist in bone and joint disorders, sports injuries.'
            }
        ]
        
        for data in doctors_data:
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password='doctor123',
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    phone=data['phone'],
                    role='doctor'
                )
                Doctor.objects.create(
                    user=user,
                    specialization=data['specialization'],
                    qualification=data['qualification'],
                    experience_years=data['experience_years'],
                    clinic_hospital=data['clinic_hospital'],
                    consultation_fee=data['consultation_fee'],
                    bio=data['bio']
                )
                self.stdout.write(f"  Created doctor: {data['username']}")

    def create_hospitals(self):
        self.stdout.write('Creating sample hospitals...')
        
        hospitals_data = [
            {
                'name': 'Apollo Hospital',
                'address': 'Sahar Road, Andheri East',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'contact_number': '022-26834343',
                'email': 'apollo.mumbai@apollo.com',
                'has_emergency': True,
                'has_ambulance': True,
                'beds_available': 50,
                'latitude': 19.0896,
                'longitude': 72.8656
            },
            {
                'name': 'Fortis Hospital',
                'address': 'Sector 62, Phase VIII',
                'city': 'Delhi',
                'state': 'Delhi',
                'contact_number': '011-42765000',
                'email': 'fortis.delhi@fortis.in',
                'has_emergency': True,
                'has_ambulance': True,
                'beds_available': 45,
                'latitude': 28.6139,
                'longitude': 77.2090
            },
            {
                'name': 'Max Hospital',
                'address': 'Saket, South Delhi',
                'city': 'Delhi',
                'state': 'Delhi',
                'contact_number': '011-26515050',
                'email': 'max.saket@max.in',
                'has_emergency': True,
                'has_ambulance': True,
                'beds_available': 60,
                'latitude': 28.5244,
                'longitude': 77.2066
            },
            {
                'name': 'Manipal Hospital',
                'address': 'HAL Airport Road',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'contact_number': '080-25023344',
                'email': 'manipal.bangalore@manipal.com',
                'has_emergency': True,
                'has_ambulance': True,
                'beds_available': 40,
                'latitude': 12.9716,
                'longitude': 77.5946
            },
            {
                'name': 'Medanta Hospital',
                'address': 'Sector 38, Gurgaon',
                'city': 'Gurgaon',
                'state': 'Haryana',
                'contact_number': '0124-4141414',
                'email': 'medanta@medanta.org',
                'has_emergency': True,
                'has_ambulance': True,
                'beds_available': 70,
                'latitude': 28.4272,
                'longitude': 76.9970
            },
            {
                'name': 'Kokilaben Hospital',
                'address': 'Andheri West',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'contact_number': '022-42356789',
                'email': 'kokilaben@hospital.com',
                'has_emergency': True,
                'has_ambulance': True,
                'beds_available': 55,
                'latitude': 19.1374,
                'longitude': 72.8339
            },
            {
                'name': 'City Clinic',
                'address': 'MG Road',
                'city': 'Pune',
                'state': 'Maharashtra',
                'contact_number': '020-25123456',
                'email': 'city.clinic@pune.com',
                'has_emergency': False,
                'has_ambulance': False,
                'beds_available': 15,
                'latitude': 18.5204,
                'longitude': 73.8567
            },
            {
                'name': 'Rainbow Children Hospital',
                'address': 'Banjara Hills',
                'city': 'Hyderabad',
                'state': 'Telangana',
                'contact_number': '040-44557788',
                'email': 'rainbow@rainbow.in',
                'has_emergency': True,
                'has_ambulance': True,
                'beds_available': 35,
                'latitude': 17.4219,
                'longitude': 78.4487
            }
        ]
        
        for data in hospitals_data:
            if not Hospital.objects.filter(name=data['name'], city=data['city']).exists():
                Hospital.objects.create(**data)
                self.stdout.write(f"  Created hospital: {data['name']}")
