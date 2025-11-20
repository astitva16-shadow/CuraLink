from django.contrib import admin
from .models import Hospital


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'contact_number', 'has_emergency', 'has_ambulance', 'rating']
    list_filter = ['has_emergency', 'has_ambulance', 'city']
    search_fields = ['name', 'city', 'address']
    ordering = ['-has_emergency', 'name']
