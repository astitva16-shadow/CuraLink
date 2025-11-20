"""
URL Configuration for API App
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'doctors', views.DoctorViewSet, basename='doctor')
router.register(r'hospitals', views.HospitalViewSet, basename='hospital')
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')
router.register(r'consultation-summaries', views.ConsultationSummaryViewSet, basename='consultation-summary')

urlpatterns = [
    path('', include(router.urls)),
]
