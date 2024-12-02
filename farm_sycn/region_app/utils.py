from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_coordinates(village, cell, sector, district, province):
    address = f"{village}, {cell}, {sector}, {district}, {province}, Rwanda"
    
    geolocator = Nominatim(user_agent="farmSync_v1.0")
    try:
        location = geolocator.geocode(address)
        if location:
            return {"latitude": location.latitude, "longitude": location.longitude}
        else:
            return None 
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error: {e}")
        return None
