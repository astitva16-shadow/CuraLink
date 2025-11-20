"""
Appointment Models for CuraLink
"""
from django.db import models
from django.conf import settings
from accounts.models import Doctor


class Appointment(models.Model):
    """
    Appointment Model - manages patient-doctor appointments
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_appointments'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='doctor_appointments'
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    symptoms = models.TextField(help_text="Brief description of symptoms or reason for consultation")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Additional notes from patient")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
    
    def __str__(self):
        return f"Appointment: {self.patient.username} with Dr. {self.doctor.user.get_full_name()} on {self.appointment_date}"


class ConsultationSummary(models.Model):
    """
    Consultation Summary - stores doctor's notes after appointment completion
    """
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='consultation_summary'
    )
    diagnosis = models.TextField(help_text="Doctor's diagnosis")
    prescribed_medicines = models.TextField(help_text="List of prescribed medicines with dosage")
    instructions = models.TextField(help_text="Instructions for medication and lifestyle")
    diet_recommendations = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Summary for {self.appointment}"
