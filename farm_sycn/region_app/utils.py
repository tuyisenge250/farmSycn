from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_coordinates(village, cell, sector, district, province):
    """
    Get the geographical coordinates (latitude and longitude) of a location.

    Parameters:
    - village (str): The name of the village.
    - cell (str): The name of the cell.
    - sector (str): The name of the sector.
    - district (str): The name of the district.
    - province (str): The name of the province.

    Returns:
    - dict: A dictionary with 'latitude' and 'longitude' keys if successful.
    - None: If the geocoding fails or an error occurs.
    """
    address = f"{village}, {cell}, {sector}, {district}, {province}, Rwanda"
    geolocator = Nominatim(user_agent="farmSync_v1.0")

    try:
        location = geolocator.geocode(address, timeout=10)  # Added timeout for better error handling
        if location:
            return {"latitude": location.latitude, "longitude": location.longitude}
        else:
            print(f"Could not find coordinates for the address: {address}")
            return None
    except GeocoderTimedOut:
        print("Geocoding service timed out. Please try again later.")
        return None
    except GeocoderServiceError as e:
        print(f"Geocoding service error: {e}")
        return None

