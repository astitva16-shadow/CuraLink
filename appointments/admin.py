from django.contrib import admin
from .models import Appointment, ConsultationSummary


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['status', 'appointment_date']
    search_fields = ['patient__username', 'doctor__user__username']
    ordering = ['-appointment_date', '-appointment_time']


@admin.register(ConsultationSummary)
class ConsultationSummaryAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'follow_up_required', 'follow_up_date', 'created_at']
    search_fields = ['appointment__patient__username', 'diagnosis']
