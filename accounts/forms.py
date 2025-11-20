"""
Forms for User Authentication and Registration
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Doctor


class PatientRegistrationForm(UserCreationForm):
    """Registration form for patients"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)
    age = forms.IntegerField(required=True, min_value=1, max_value=120)
    gender = forms.ChoiceField(choices=Patient.GENDER_CHOICES, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.role = 'patient'
        
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                age=self.cleaned_data['age'],
                gender=self.cleaned_data['gender'],
                address=self.cleaned_data.get('address', '')
            )
        return user


class DoctorRegistrationForm(UserCreationForm):
    """Registration form for doctors"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)
    specialization = forms.ChoiceField(choices=Doctor.SPECIALIZATION_CHOICES, required=True)
    qualification = forms.CharField(max_length=200, required=True)
    experience_years = forms.IntegerField(required=True, min_value=0, max_value=50)
    clinic_hospital = forms.CharField(max_length=200, required=True)
    consultation_fee = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.role = 'doctor'
        
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                specialization=self.cleaned_data['specialization'],
                qualification=self.cleaned_data['qualification'],
                experience_years=self.cleaned_data['experience_years'],
                clinic_hospital=self.cleaned_data['clinic_hospital'],
                consultation_fee=self.cleaned_data['consultation_fee'],
                bio=self.cleaned_data.get('bio', '')
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
