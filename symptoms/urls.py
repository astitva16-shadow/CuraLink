"""
URL Configuration for Symptoms App
"""
from django.urls import path
from . import views

app_name = 'symptoms'

urlpatterns = [
    path('', views.symptom_checker, name='symptom_checker'),
]
