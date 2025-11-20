"""
URL Configuration for Hospitals App
"""
from django.urls import path
from . import views

app_name = 'hospitals'

urlpatterns = [
    path('', views.hospital_list, name='hospital_list'),
    path('nearby/', views.nearby_hospitals, name='nearby_hospitals'),
    path('emergency/', views.emergency_page, name='emergency'),
    path('<int:pk>/', views.hospital_detail, name='hospital_detail'),
]
