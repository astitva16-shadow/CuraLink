# 🌍 GPS-Based Nearby Hospital Detection - Feature Guide

## Overview

CuraLink now includes **live GPS-based hospital detection** that allows users to find nearby hospitals within a configurable radius using their device's location services.

---

## ✨ Key Features

### 1. **Real-Time Location Detection**
- Uses browser's `navigator.geolocation` API
- High accuracy GPS positioning
- User permission-based access

### 2. **Distance Calculation**
- Haversine formula for accurate distance calculation
- Accounts for Earth's curvature
- Results in kilometers with 2 decimal precision

### 3. **Smart Filtering**
- Default search radius: 10 km (configurable)
- Sorted by distance (nearest first)
- Excludes hospitals without GPS coordinates

### 4. **Rich Results Display**
- Distance badge on each card
- Emergency and ambulance service indicators
- Direct Google Maps integration for directions
- Hospital details (beds, rating, contact)

---

## 🔧 Technical Implementation

### Backend Components

#### 1. **Hospital Model** (`hospitals/models.py`)
```python
latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
```

#### 2. **Distance Calculation** (`hospitals/views.py`)
```python
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate great circle distance between two points
    Returns distance in kilometers
    """
    # Haversine formula implementation
    # Radius of Earth: 6371 km
```

#### 3. **Nearby Hospitals API** (`/hospitals/nearby/`)
- **Method**: GET
- **Parameters**:
  - `lat` (required): User's latitude
  - `lon` (required): User's longitude
  - `radius` (optional): Search radius in km (default: 10)

- **Response Format**:
```json
{
    "success": true,
    "count": 3,
    "user_location": {
        "latitude": 19.0760,
        "longitude": 72.8777
    },
    "radius_km": 10,
    "hospitals": [
        {
            "id": 1,
            "name": "Apollo Hospital",
            "address": "Sahar Road, Andheri East",
            "city": "Mumbai",
            "state": "Maharashtra",
            "contact_number": "022-26834343",
            "has_emergency": true,
            "has_ambulance": true,
            "beds_available": 50,
            "rating": 4.5,
            "latitude": 19.0896,
            "longitude": 72.8656,
            "distance": 2.34
        }
    ]
}
```

### Frontend Components

#### 1. **UI Elements** (`templates/hospitals/hospital_list.html`)
- **"Find Nearby Hospitals" Button**: Triggers GPS detection
- **Location Status Div**: Shows progress and messages
- **Dynamic Hospital Cards**: Rendered via JavaScript

#### 2. **JavaScript Implementation**
```javascript
// 1. Check geolocation support
if (!navigator.geolocation) {
    // Show error message
}

// 2. Request user location
navigator.geolocation.getCurrentPosition(
    successCallback,
    errorCallback,
    options
);

// 3. Fetch nearby hospitals via AJAX
fetch(`/hospitals/nearby/?lat=${lat}&lon=${lon}&radius=10`)
    .then(response => response.json())
    .then(data => {
        // Render hospital cards dynamically
    });
```

#### 3. **Error Handling**
- Permission denied
- Position unavailable
- Timeout errors
- Network errors

---

## 📍 Sample Hospital GPS Coordinates

| Hospital | City | Latitude | Longitude |
|----------|------|----------|-----------|
| Apollo Hospital | Mumbai | 19.0896 | 72.8656 |
| Kokilaben Hospital | Mumbai | 19.1374 | 72.8339 |
| Fortis Hospital | Delhi | 28.6139 | 77.2090 |
| Max Hospital | Delhi | 28.5244 | 77.2066 |
| Manipal Hospital | Bangalore | 12.9716 | 77.5946 |
| Medanta Hospital | Gurgaon | 28.4272 | 76.9970 |
| City Clinic | Pune | 18.5204 | 73.8567 |
| Rainbow Hospital | Hyderabad | 17.4219 | 78.4487 |

---

## 🚀 Usage Guide

### For Users

1. **Navigate to Hospitals Page**
   ```
   http://127.0.0.1:8000/hospitals/
   ```

2. **Click "Find Nearby Hospitals" Button**
   - Browser will prompt for location permission
   - Click "Allow" to grant access

3. **View Results**
   - Hospitals displayed sorted by distance
   - Green distance badge shows km from your location
   - Click "Directions" to open Google Maps

### For Developers

#### Testing the API Directly
```bash
# Replace with your coordinates
curl "http://127.0.0.1:8000/hospitals/nearby/?lat=19.0760&lon=72.8777&radius=10"
```

#### Adding New Hospitals with GPS
```python
Hospital.objects.create(
    name='New Hospital',
    address='123 Main St',
    city='Mumbai',
    state='Maharashtra',
    contact_number='022-12345678',
    has_emergency=True,
    has_ambulance=True,
    beds_available=30,
    latitude=19.1000,  # Add GPS coordinates
    longitude=72.9000
)
```

#### Customizing Search Radius
```javascript
// In hospital_list.html, change the radius parameter
fetch(`/hospitals/nearby/?lat=${lat}&lon=${lon}&radius=15`)  // 15 km
```

---

## 🎨 UI Features

### Visual Indicators

1. **Distance Badge** - Green badge showing distance in km
2. **Border Highlight** - Green border on nearby hospital cards
3. **Emergency Badge** - Red badge for emergency services
4. **Ambulance Badge** - Warning badge for ambulance availability
5. **Loading Spinner** - Shows during location detection

### Buttons

- **Find Nearby Hospitals** - Primary action button
- **View Details** - Navigate to hospital detail page
- **Directions** - Opens Google Maps with directions

---

## 🔐 Privacy & Security

### User Location Handling

1. **Permission-Based Access**
   - Browser asks user for permission
   - No location stored on server
   - Location used only for distance calculation

2. **HTTPS Requirement**
   - Modern browsers require HTTPS for geolocation
   - For development: `http://localhost` is allowed
   - For production: Must use HTTPS

3. **Data Privacy**
   - User coordinates sent via GET request
   - No persistent storage of user location
   - Temporary data for search only

---

## 📊 Distance Calculation Formula

### Haversine Formula

The Haversine formula calculates the shortest distance between two points on a sphere:

```
a = sin²(Δφ/2) + cos(φ1) × cos(φ2) × sin²(Δλ/2)
c = 2 × atan2(√a, √(1−a))
d = R × c

where:
φ = latitude in radians
λ = longitude in radians
R = Earth's radius (6371 km)
```

### Accuracy

- **Earth's radius**: 6371 km (mean radius)
- **Precision**: ±0.01 km (10 meters)
- **Valid for**: Distances up to ~100 km
- **Performance**: O(n) where n = number of hospitals

---

## 🧪 Testing Scenarios

### Manual Testing

1. **Permission Granted**
   - Click button → Allow permission → View results

2. **Permission Denied**
   - Click button → Deny permission → See error message

3. **No Hospitals Nearby**
   - Test from location far from all hospitals
   - Should show "No hospitals found" message

4. **Multiple Hospitals**
   - Test from major city (Mumbai, Delhi)
   - Should show multiple results sorted by distance

### Unit Testing

```python
from hospitals.views import haversine_distance

# Test distance calculation
def test_haversine_distance():
    # Mumbai to Bangalore (approximate)
    distance = haversine_distance(19.0760, 72.8777, 12.9716, 77.5946)
    assert 820 < distance < 850  # ~840 km
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Location Permission Denied
**Error**: "Location access denied"
**Solution**: 
- Check browser location settings
- Enable location services on device
- Try in Chrome/Firefox (better support)

#### 2. No Hospitals Found
**Error**: "No hospitals found within 10 km"
**Solution**:
- Increase radius in code
- Check if hospitals have GPS coordinates
- Verify your location is correct

#### 3. Geolocation Not Supported
**Error**: "Geolocation is not supported"
**Solution**:
- Use modern browser (Chrome 50+, Firefox 55+, Safari 10+)
- Check if running on HTTPS (production)

#### 4. Network Error
**Error**: "Error fetching nearby hospitals"
**Solution**:
- Check if Django server is running
- Verify URL endpoint is correct
- Check browser console for details

---

## 🔄 API Integration

### Using the Nearby API in Other Apps

#### Mobile App Example (React Native)
```javascript
import * as Location from 'expo-location';

async function findNearbyHospitals() {
    let { status } = await Location.requestForegroundPermissionsAsync();
    
    if (status !== 'granted') {
        return;
    }
    
    let location = await Location.getCurrentPositionAsync({});
    
    const response = await fetch(
        `https://api.curalink.com/hospitals/nearby/?lat=${location.coords.latitude}&lon=${location.coords.longitude}&radius=10`
    );
    
    const data = await response.json();
    return data.hospitals;
}
```

#### Python Client Example
```python
import requests

def get_nearby_hospitals(lat, lon, radius=10):
    url = f"http://127.0.0.1:8000/hospitals/nearby/"
    params = {
        'lat': lat,
        'lon': lon,
        'radius': radius
    }
    
    response = requests.get(url, params=params)
    return response.json()

# Example usage
hospitals = get_nearby_hospitals(19.0760, 72.8777)
for hospital in hospitals['hospitals']:
    print(f"{hospital['name']} - {hospital['distance']} km")
```

---

## 🌟 Advanced Features (Future Enhancements)

### Potential Improvements

1. **Interactive Map View**
   - Integrate Leaflet or Google Maps
   - Show hospital markers on map
   - Draw radius circle

2. **Filters for Nearby Results**
   - Emergency only
   - Minimum rating
   - Specialization filter

3. **Save Favorite Hospitals**
   - Bookmark nearby hospitals
   - Quick access to frequently visited

4. **Route Planning**
   - Multi-hospital route
   - Estimated travel time
   - Traffic consideration

5. **Real-Time Updates**
   - Live bed availability
   - Wait time estimates
   - Emergency room status

---

## 📱 Browser Compatibility

| Browser | Version | Geolocation Support |
|---------|---------|---------------------|
| Chrome | 50+ | ✅ Full Support |
| Firefox | 55+ | ✅ Full Support |
| Safari | 10+ | ✅ Full Support |
| Edge | 79+ | ✅ Full Support |
| Opera | 37+ | ✅ Full Support |
| IE 11 | - | ⚠️ Limited |

---

## 📝 Configuration Options

### Modify Search Radius
Edit `templates/hospitals/hospital_list.html`:
```javascript
fetch(`/hospitals/nearby/?lat=${lat}&lon=${lon}&radius=15`)  // Change 15
```

### Adjust Geolocation Options
```javascript
navigator.geolocation.getCurrentPosition(
    successCallback,
    errorCallback,
    {
        enableHighAccuracy: true,  // Use GPS (slower but accurate)
        timeout: 10000,            // 10 seconds timeout
        maximumAge: 0              // No cached location
    }
);
```

### Database Field Precision
Edit `hospitals/models.py`:
```python
latitude = models.DecimalField(max_digits=10, decimal_places=7)  # More precision
longitude = models.DecimalField(max_digits=10, decimal_places=7)
```

---

## 🎓 Educational Use

This feature demonstrates:

1. **RESTful API Design** - Clean endpoint with query parameters
2. **Geolocation API** - Browser-based location services
3. **Haversine Formula** - Mathematical distance calculation
4. **AJAX/Fetch** - Asynchronous data retrieval
5. **Dynamic DOM Manipulation** - JavaScript rendering
6. **User Experience** - Loading states, error handling
7. **Privacy Considerations** - Permission-based features

---

## 📞 Support

For issues or questions:
- Check browser console for JavaScript errors
- Verify Django server logs for backend errors
- Review this guide for common solutions
- Test API endpoint directly with curl

---

**Feature Version**: 1.0
**Last Updated**: November 2025
**Compatible With**: CuraLink v1.0+

🏥 **CuraLink - Your Bridge to Better Health** 💙
