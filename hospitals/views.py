"""
Views for Hospital Management
"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Hospital
import math


def hospital_list(request):
    """
    List all hospitals with filtering options
    """
    hospitals = Hospital.objects.all()
    
    # Filter by city
    city = request.GET.get('city', '')
    if city:
        hospitals = hospitals.filter(city__icontains=city)
    
    # Filter by emergency services
    emergency_only = request.GET.get('emergency', '')
    if emergency_only:
        hospitals = hospitals.filter(has_emergency=True)
    
    # Get unique cities for filter dropdown
    cities = Hospital.objects.values_list('city', flat=True).distinct().order_by('city')
    
    # Pagination
    paginator = Paginator(hospitals, 9)  # 9 hospitals per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'cities': cities,
        'selected_city': city,
        'emergency_only': emergency_only,
    }
    return render(request, 'hospitals/hospital_list.html', context)


def hospital_detail(request, pk):
    """
    Display detailed information about a specific hospital
    """
    hospital = get_object_or_404(Hospital, pk=pk)
    context = {
        'hospital': hospital
    }
    return render(request, 'hospitals/hospital_detail.html', context)


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r


@require_http_methods(["GET"])
def nearby_hospitals(request):
    """
    API endpoint to find nearby hospitals based on user's GPS location
    Query params: lat, lon, radius (default 100 km)
    Returns: JSON list of nearby hospitals sorted by distance
    """
    try:
        user_lat = float(request.GET.get('lat'))
        user_lon = float(request.GET.get('lon'))
        radius = float(request.GET.get('radius', 100))  # default 100 km
    except (TypeError, ValueError):
        return JsonResponse({
            'error': 'Invalid parameters. Required: lat, lon. Optional: radius (km)'
        }, status=400)
    
    # Get all hospitals with GPS coordinates
    hospitals = Hospital.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    
    # Calculate distance for each hospital
    nearby = []
    for hospital in hospitals:
        distance = haversine_distance(
            user_lat, user_lon,
            float(hospital.latitude), float(hospital.longitude)
        )
        
        if distance <= radius:
            nearby.append({
                'id': hospital.id,
                'name': hospital.name,
                'address': hospital.address,
                'city': hospital.city,
                'state': hospital.state,
                'contact_number': hospital.contact_number,
                'has_emergency': hospital.has_emergency,
                'has_ambulance': hospital.has_ambulance,
                'beds_available': hospital.beds_available,
                'rating': float(hospital.rating),
                'latitude': float(hospital.latitude),
                'longitude': float(hospital.longitude),
                'distance': round(distance, 2)
            })
    
    # Sort by distance
    nearby.sort(key=lambda x: x['distance'])
    
    return JsonResponse({
        'success': True,
        'count': len(nearby),
        'user_location': {
            'latitude': user_lat,
            'longitude': user_lon
        },
        'radius_km': radius,
        'hospitals': nearby
    })


def emergency_page(request):
    """
    Emergency page showing emergency hospitals and ambulance services
    """
    emergency_hospitals = Hospital.objects.filter(has_emergency=True)[:10]
    
    context = {
        'emergency_hospitals': emergency_hospitals,
        'emergency_number': '112',  # Configurable emergency number
        'ambulance_number': '108',
    }
    return render(request, 'hospitals/emergency.html', context)
