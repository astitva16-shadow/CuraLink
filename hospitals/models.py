"""
Hospital Models for CuraLink
"""
from django.db import models


class Hospital(models.Model):
    """
    Hospital Model - stores information about hospitals and clinics
    """
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    district = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, default='')
    contact_number = models.CharField(max_length=15, blank=True, default='')
    email = models.EmailField(blank=True)
    has_emergency = models.BooleanField(default=False, help_text="Does this hospital have emergency services?")
    has_ambulance = models.BooleanField(default=False)
    beds_available = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    facility_type = models.CharField(max_length=100, blank=True, default='', help_text="PHC/CHC/District Hospital/etc")
    website = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-has_emergency', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.city}"
