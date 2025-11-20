"""
Forms for Appointment Management
"""
from django import forms
from .models import Appointment, ConsultationSummary
from accounts.models import Doctor
from django.utils import timezone


class AppointmentForm(forms.ModelForm):
    """Form for booking appointments"""
    
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'symptoms', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'symptoms': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_available=True)
        self.fields['doctor'].widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')
        
        if appointment_date and appointment_time:
            # Check if appointment is not in the past
            from datetime import datetime, date
            today = date.today()
            if appointment_date < today:
                raise forms.ValidationError("Cannot book appointments in the past.")
            
            # If today, check if time hasn't passed
            if appointment_date == today:
                current_time = timezone.now().time()
                if appointment_time < current_time:
                    raise forms.ValidationError("Cannot book appointments for past times today.")
        
        return cleaned_data


class ConsultationSummaryForm(forms.ModelForm):
    """Form for doctors to create consultation summaries"""
    
    class Meta:
        model = ConsultationSummary
        fields = ['diagnosis', 'prescribed_medicines', 'instructions', 'diet_recommendations', 
                  'follow_up_required', 'follow_up_date']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'prescribed_medicines': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'diet_recommendations': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
