"""
Views for Appointment Management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from accounts.models import Doctor
from .models import Appointment, ConsultationSummary
from .forms import AppointmentForm, ConsultationSummaryForm


def doctor_list(request):
    """
    List all doctors with filtering by specialization
    """
    doctors = Doctor.objects.filter(is_available=True)
    
    # Filter by specialization
    specialization = request.GET.get('specialization', '')
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    
    # Pagination
    paginator = Paginator(doctors, 9)  # 9 doctors per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all specializations for filter
    specializations = Doctor.SPECIALIZATION_CHOICES
    
    context = {
        'page_obj': page_obj,
        'specializations': specializations,
        'selected_specialization': specialization,
    }
    return render(request, 'appointments/doctor_list.html', context)


def doctor_detail(request, pk):
    """
    Display detailed information about a specific doctor
    """
    doctor = get_object_or_404(Doctor, pk=pk)
    context = {
        'doctor': doctor
    }
    return render(request, 'appointments/doctor_detail.html', context)


@login_required
def book_appointment(request, doctor_id=None):
    """
    Book an appointment with a doctor
    """
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointments:appointment_confirmation', pk=appointment.pk)
    else:
        initial_data = {}
        if doctor_id:
            doctor = get_object_or_404(Doctor, pk=doctor_id)
            initial_data['doctor'] = doctor
        form = AppointmentForm(initial=initial_data)
    
    return render(request, 'appointments/book_appointment.html', {'form': form})


@login_required
def appointment_confirmation(request, pk):
    """
    Display appointment confirmation details
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Ensure user can only view their own appointments
    if appointment.patient != request.user and appointment.doctor.user != request.user:
        messages.error(request, 'You do not have permission to view this appointment.')
        return redirect('home')
    
    context = {
        'appointment': appointment
    }
    return render(request, 'appointments/appointment_confirmation.html', context)


@login_required
def my_appointments(request):
    """
    List appointments for current user (patient or doctor)
    """
    if request.user.role == 'patient':
        appointments = Appointment.objects.filter(patient=request.user)
    elif request.user.role == 'doctor':
        try:
            doctor_profile = request.user.doctor_profile
            appointments = Appointment.objects.filter(doctor=doctor_profile)
        except:
            appointments = Appointment.objects.none()
    else:
        appointments = Appointment.objects.none()
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        appointments = appointments.filter(status=status)
    
    context = {
        'appointments': appointments,
        'status_choices': Appointment.STATUS_CHOICES,
        'selected_status': status,
    }
    return render(request, 'appointments/my_appointments.html', context)


@login_required
def update_appointment_status(request, pk):
    """
    Update appointment status (for doctors)
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Only the assigned doctor can update status
    if request.user.role != 'doctor' or appointment.doctor != request.user.doctor_profile:
        messages.error(request, 'You do not have permission to update this appointment.')
        return redirect('appointments:my_appointments')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Appointment status updated to {appointment.get_status_display()}.')
    
    return redirect('appointments:my_appointments')


@login_required
def cancel_appointment(request, pk):
    """
    Cancel an appointment
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Only patient or doctor can cancel
    if appointment.patient != request.user and (request.user.role != 'doctor' or appointment.doctor != request.user.doctor_profile):
        messages.error(request, 'You do not have permission to cancel this appointment.')
        return redirect('appointments:my_appointments')
    
    if appointment.status not in ['completed', 'cancelled']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel this appointment.')
    
    return redirect('appointments:my_appointments')


@login_required
def create_consultation_summary(request, appointment_id):
    """
    Create or update consultation summary (doctors only)
    """
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    # Only the assigned doctor can create summary
    if request.user.role != 'doctor' or appointment.doctor != request.user.doctor_profile:
        messages.error(request, 'You do not have permission to create a summary for this appointment.')
        return redirect('appointments:my_appointments')
    
    # Check if summary already exists
    try:
        summary = appointment.consultation_summary
        is_new = False
    except ConsultationSummary.DoesNotExist:
        summary = None
        is_new = True
    
    if request.method == 'POST':
        form = ConsultationSummaryForm(request.POST, instance=summary)
        if form.is_valid():
            summary = form.save(commit=False)
            summary.appointment = appointment
            summary.save()
            
            # Update appointment status to completed
            appointment.status = 'completed'
            appointment.save()
            
            messages.success(request, 'Consultation summary saved successfully!')
            return redirect('appointments:my_appointments')
    else:
        form = ConsultationSummaryForm(instance=summary)
    
    context = {
        'form': form,
        'appointment': appointment,
        'is_new': is_new,
    }
    return render(request, 'appointments/create_consultation_summary.html', context)


@login_required
def view_consultation_summary(request, appointment_id):
    """
    View consultation summary
    """
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    # Only patient or doctor can view
    if appointment.patient != request.user and (request.user.role != 'doctor' or appointment.doctor != request.user.doctor_profile):
        messages.error(request, 'You do not have permission to view this summary.')
        return redirect('appointments:my_appointments')
    
    try:
        summary = appointment.consultation_summary
    except ConsultationSummary.DoesNotExist:
        messages.error(request, 'No consultation summary available for this appointment.')
        return redirect('appointments:my_appointments')
    
    context = {
        'appointment': appointment,
        'summary': summary,
    }
    return render(request, 'appointments/view_consultation_summary.html', context)


@login_required
def print_consultation_summary(request, appointment_id):
    """
    Print-friendly view of consultation summary
    """
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    # Only patient or doctor can view
    if appointment.patient != request.user and (request.user.role != 'doctor' or appointment.doctor != request.user.doctor_profile):
        messages.error(request, 'You do not have permission to view this summary.')
        return redirect('appointments:my_appointments')
    
    try:
        summary = appointment.consultation_summary
    except ConsultationSummary.DoesNotExist:
        messages.error(request, 'No consultation summary available for this appointment.')
        return redirect('appointments:my_appointments')
    
    context = {
        'appointment': appointment,
        'summary': summary,
    }
    return render(request, 'appointments/print_consultation_summary.html', context)
