from geopy.geocoders import Nominatim

def GeoCountry(latitude, longitude):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.reverse((latitude, longitude), language="en")
# Verifica si location es None antes de acceder a location.raw
    if location is not None and 'address' in location.raw and 'country' in location.raw['address']:
        country = location.raw['address']['country']
    else:
        country = "Fuera de Fronteras"
    return country
