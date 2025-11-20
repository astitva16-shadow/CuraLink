"""
API Views using Django REST Framework
"""
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from accounts.models import Doctor
from hospitals.models import Hospital
from appointments.models import Appointment, ConsultationSummary
from .serializers import (
    DoctorSerializer, HospitalSerializer, AppointmentSerializer,
    ConsultationSummarySerializer
)


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing doctors.
    GET /api/doctors/ - List all doctors
    GET /api/doctors/<id>/ - Get specific doctor
    Filter by specialization: /api/doctors/?specialization=cardiology
    """
    queryset = Doctor.objects.filter(is_available=True)
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'specialization', 'clinic_hospital']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        specialization = self.request.query_params.get('specialization', None)
        if specialization:
            queryset = queryset.filter(specialization=specialization)
        return queryset


class HospitalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing hospitals.
    GET /api/hospitals/ - List all hospitals
    GET /api/hospitals/<id>/ - Get specific hospital
    Filter by city: /api/hospitals/?city=Mumbai
    Filter by emergency: /api/hospitals/?emergency=true
    """
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city', 'address']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get('city', None)
        emergency = self.request.query_params.get('emergency', None)
        
        if city:
            queryset = queryset.filter(city__icontains=city)
        if emergency:
            queryset = queryset.filter(has_emergency=True)
        
        return queryset


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing appointments.
    GET /api/appointments/ - List user's appointments
    POST /api/appointments/ - Create new appointment
    GET /api/appointments/<id>/ - Get specific appointment
    PUT /api/appointments/<id>/ - Update appointment
    DELETE /api/appointments/<id>/ - Cancel appointment
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return appointments based on user role:
        - Patients see their own appointments
        - Doctors see appointments where they are the doctor
        """
        user = self.request.user
        if user.role == 'patient':
            return Appointment.objects.filter(patient=user)
        elif user.role == 'doctor':
            try:
                doctor_profile = user.doctor_profile
                return Appointment.objects.filter(doctor=doctor_profile)
            except:
                return Appointment.objects.none()
        return Appointment.objects.none()
    
    def perform_create(self, serializer):
        """Create appointment with current user as patient"""
        serializer.save(patient=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        """Cancel an appointment"""
        appointment = self.get_object()
        
        # Check permissions
        if appointment.patient != request.user and (request.user.role != 'doctor' or appointment.doctor != request.user.doctor_profile):
            return Response(
                {'error': 'You do not have permission to cancel this appointment.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if appointment.status not in ['completed', 'cancelled']:
            appointment.status = 'cancelled'
            appointment.save()
            return Response({'status': 'Appointment cancelled successfully.'})
        else:
            return Response(
                {'error': 'Cannot cancel this appointment.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        """Update appointment status (doctors only)"""
        appointment = self.get_object()
        
        # Only doctor can update status
        if request.user.role != 'doctor' or appointment.doctor != request.user.doctor_profile:
            return Response(
                {'error': 'Only the assigned doctor can update appointment status.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        valid_statuses = dict(Appointment.STATUS_CHOICES).keys()
        
        if new_status in valid_statuses:
            appointment.status = new_status
            appointment.save()
            serializer = self.get_serializer(appointment)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Invalid status value.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ConsultationSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing consultation summaries.
    GET /api/consultation-summaries/ - List accessible summaries
    GET /api/consultation-summaries/<id>/ - Get specific summary
    """
    serializer_class = ConsultationSummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return summaries based on user role:
        - Patients see summaries of their appointments
        - Doctors see summaries of appointments where they are the doctor
        """
        user = self.request.user
        if user.role == 'patient':
            return ConsultationSummary.objects.filter(appointment__patient=user)
        elif user.role == 'doctor':
            try:
                doctor_profile = user.doctor_profile
                return ConsultationSummary.objects.filter(appointment__doctor=doctor_profile)
            except:
                return ConsultationSummary.objects.none()
        return ConsultationSummary.objects.none()
