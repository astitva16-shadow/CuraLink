"""
Serializers for REST API
"""
from rest_framework import serializers
from accounts.models import Doctor, User
from hospitals.models import Hospital
from appointments.models import Appointment, ConsultationSummary


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone']
        read_only_fields = ['id']


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model"""
    user = UserSerializer(read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'specialization_display', 'qualification', 
                  'experience_years', 'clinic_hospital', 'consultation_fee', 'bio', 
                  'rating', 'is_available']
        read_only_fields = ['id', 'rating']


class HospitalSerializer(serializers.ModelSerializer):
    """Serializer for Hospital model"""
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'address', 'city', 'state', 'contact_number', 'email',
                  'has_emergency', 'has_ambulance', 'beds_available', 'description', 
                  'website', 'rating', 'latitude', 'longitude']
        read_only_fields = ['id', 'rating']


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model"""
    patient = UserSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'doctor_id', 'appointment_date', 
                  'appointment_time', 'symptoms', 'status', 'status_display', 
                  'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'patient', 'status', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate appointment data"""
        from datetime import date, datetime
        from django.utils import timezone
        
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')
        
        if appointment_date and appointment_time:
            today = date.today()
            if appointment_date < today:
                raise serializers.ValidationError("Cannot book appointments in the past.")
            
            if appointment_date == today:
                current_time = timezone.now().time()
                if appointment_time < current_time:
                    raise serializers.ValidationError("Cannot book appointments for past times today.")
        
        return data
    
    def create(self, validated_data):
        """Create appointment with current user as patient"""
        doctor_id = validated_data.pop('doctor_id')
        doctor = Doctor.objects.get(pk=doctor_id)
        validated_data['doctor'] = doctor
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)


class ConsultationSummarySerializer(serializers.ModelSerializer):
    """Serializer for Consultation Summary"""
    appointment = AppointmentSerializer(read_only=True)
    
    class Meta:
        model = ConsultationSummary
        fields = ['id', 'appointment', 'diagnosis', 'prescribed_medicines', 
                  'instructions', 'diet_recommendations', 'follow_up_required', 
                  'follow_up_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
