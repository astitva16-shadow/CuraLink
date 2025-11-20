# 🎯 Quick Test Guide - GPS Hospital Finder

## Testing the GPS Feature (5 Minutes)

### Step 1: Access the Hospitals Page
```
URL: http://127.0.0.1:8000/hospitals/
```

### Step 2: Look for the GPS Section
You'll see a highlighted card at the top with:
```
🌍 Find Hospitals Near You
Use your current location to find nearby hospitals within 10 km
[Find Nearby Hospitals Button]
```

### Step 3: Click the Button
- Browser will prompt: "curalink wants to know your location"
- Click **"Allow"**

### Step 4: Wait for Results
- Loading message appears: "Getting your location..."
- Success message: "Found X hospital(s) within 10 km"

### Step 5: View Results
Each hospital card shows:
- ✅ Hospital name
- ✅ **Green distance badge** (e.g., "2.34 km")
- ✅ Address and city
- ✅ Emergency/Ambulance badges
- ✅ Contact number
- ✅ Rating and beds available
- ✅ Two buttons:
  - "View Details"
  - "Directions" (opens Google Maps)

---

## 🧪 Test Without GPS Device

If you don't have a GPS-enabled device or want to test specific locations:

### Option 1: Browser Developer Tools (Fake GPS)

#### Chrome:
1. Open DevTools (F12)
2. Click the three dots menu (⋮) → More tools → Sensors
3. In Sensors tab, find "Location"
4. Select a preset (e.g., "San Francisco") or enter custom coordinates
5. Try the feature again

#### Example Custom Coordinates:
- **Mumbai**: Latitude `19.0760`, Longitude `72.8777`
- **Delhi**: Latitude `28.7041`, Longitude `77.1025`
- **Bangalore**: Latitude `12.9716`, Longitude `77.5946`

### Option 2: Direct API Testing

Test the backend API directly:

```bash
# Test Mumbai location
curl "http://127.0.0.1:8000/hospitals/nearby/?lat=19.0760&lon=72.8777&radius=10"

# Test Delhi location
curl "http://127.0.0.1:8000/hospitals/nearby/?lat=28.7041&lon=77.1025&radius=10"

# Test with larger radius (20 km)
curl "http://127.0.0.1:8000/hospitals/nearby/?lat=19.0760&lon=72.8777&radius=20"
```

Expected Response:
```json
{
    "success": true,
    "count": 2,
    "user_location": {
        "latitude": 19.076,
        "longitude": 72.8777
    },
    "radius_km": 10,
    "hospitals": [
        {
            "id": 1,
            "name": "Apollo Hospital",
            "distance": 2.34,
            ...
        }
    ]
}
```

---

## ✅ What to Verify

### Visual Elements
- [ ] Green "Find Nearby Hospitals" button appears
- [ ] Location status messages display
- [ ] Loading spinner shows during detection
- [ ] Distance badges are green
- [ ] Hospital cards have green border
- [ ] "Directions" button links to Google Maps

### Functionality
- [ ] Location permission prompt appears
- [ ] Location detected successfully
- [ ] API returns nearby hospitals
- [ ] Hospitals sorted by distance
- [ ] Distance is accurate (approximately)
- [ ] All hospital details display correctly
- [ ] Buttons work (View Details, Directions)

### Error Handling
- [ ] Permission denied shows error message
- [ ] No hospitals nearby shows appropriate message
- [ ] Network error is handled gracefully
- [ ] Button re-enables after error

---

## 🗺️ Expected Results by Location

### Near Mumbai (19.0760, 72.8777)
Should find:
- Apollo Hospital (~1-3 km)
- Kokilaben Hospital (~5-8 km)

### Near Delhi (28.7041, 77.1025)
Should find:
- Fortis Hospital (~varies)
- Max Hospital (~varies)

### Far from All Hospitals (e.g., 0.0, 0.0)
Should show:
- "No hospitals found within 10 km of your location"

---

## 🐛 Troubleshooting

### "Geolocation is not supported"
- **Issue**: Browser doesn't support geolocation
- **Fix**: Use Chrome 50+, Firefox 55+, or Safari 10+

### "Location access denied"
- **Issue**: User denied permission
- **Fix**: Reset site permissions or use private/incognito mode

### "No hospitals found"
- **Issue**: No hospitals within radius
- **Fix**: 
  - Increase radius in code (change `radius=10` to `radius=20`)
  - Add more hospitals via admin panel
  - Test from a different location

### API Returns Error 400
- **Issue**: Invalid latitude/longitude
- **Fix**: Check parameters are valid numbers
  - Latitude: -90 to 90
  - Longitude: -180 to 180

---

## 📊 Sample Test Cases

### Test Case 1: Happy Path
```
Location: Mumbai (19.0760, 72.8777)
Expected: 2 hospitals found
Distance: Apollo (~2 km), Kokilaben (~6 km)
Status: ✅ Pass
```

### Test Case 2: Edge of Radius
```
Location: Between cities
Expected: Only hospitals within exact 10 km shown
Status: ✅ Pass if correctly filtered
```

### Test Case 3: No Results
```
Location: Remote area (0.0, 0.0)
Expected: "No hospitals found" message
Status: ✅ Pass
```

### Test Case 4: Permission Denied
```
Action: Click button, deny permission
Expected: "Location access denied" error
Status: ✅ Pass if error displays
```

---

## 🎬 Demo Script

### For Presentation:

**"Let me demonstrate the GPS-based hospital finder feature..."**

1. Navigate to Hospitals page
2. Point out the highlighted GPS card
3. Click "Find Nearby Hospitals"
4. Show permission prompt and allow
5. Wait for loading (explain what's happening)
6. Show results with distance badges
7. Point out key features:
   - Distance calculation
   - Emergency badges
   - Google Maps integration
8. Click "Directions" on one hospital
9. Show Google Maps opening with route

**"This feature uses the Haversine formula to calculate accurate distances and the browser's geolocation API for privacy-first location detection."**

---

## 📱 Mobile Testing

### On Mobile Device:
1. Connect to same network as dev server
2. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Mac/Linux
   ifconfig
   ```
3. Access: `http://YOUR_IP:8000/hospitals/`
4. Test GPS (more accurate on mobile!)

### Expected Mobile Experience:
- GPS location more accurate
- Maps opens in native Google Maps app
- Touch-friendly buttons
- Responsive layout

---

## ⏱️ Performance Expectations

- **Location Detection**: 1-5 seconds
- **API Response**: <500ms
- **Rendering**: Instant
- **Total Time**: 2-10 seconds

---

## 🎓 Key Points to Highlight

1. **Privacy-First**: Location never stored
2. **Accurate**: Haversine formula accounts for Earth's curvature
3. **User-Friendly**: Clear messages and loading states
4. **Mobile-Ready**: Works on all devices
5. **Integrated**: Google Maps for directions
6. **Configurable**: Radius can be adjusted

---

**Ready to Test?** Start the server and open http://127.0.0.1:8000/hospitals/

🏥 **CuraLink - Your Bridge to Better Health** 💙
