from geopy.geocoders import Nominatim

# Función que devuelve el país de una coordenada geográfica sin usar los polígonos, pero con la limitación que solo funciona 2500 veces al dia

def GeoCountry(latitude, longitude):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.reverse((latitude, longitude), language="en")
# Verifica si location es None antes de acceder a location.raw
    if location is not None and 'address' in location.raw and 'country' in location.raw['address']:
        country = location.raw['address']['country']
    else:
        country = "Fuera de Fronteras"
    return country