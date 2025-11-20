"""
URL Configuration for Appointments App
"""
from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    # Doctor listings
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    
    # Appointment booking
    path('book/', views.book_appointment, name='book_appointment'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment_doctor'),
    path('confirmation/<int:pk>/', views.appointment_confirmation, name='appointment_confirmation'),
    
    # Manage appointments
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('<int:pk>/update-status/', views.update_appointment_status, name='update_appointment_status'),
    path('<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    
    # Consultation summaries
    path('<int:appointment_id>/create-summary/', views.create_consultation_summary, name='create_consultation_summary'),
    path('<int:appointment_id>/view-summary/', views.view_consultation_summary, name='view_consultation_summary'),
    path('<int:appointment_id>/print-summary/', views.print_consultation_summary, name='print_consultation_summary'),
]
