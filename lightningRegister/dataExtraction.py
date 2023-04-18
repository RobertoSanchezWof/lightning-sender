from shapely.geometry import Point, Polygon
from lightningRegister.constants import *
from datetime import datetime, timedelta
from lightningRegister.geoCountry import GeoCountry

# Funciones para calcular coordenadas en poligonos
def PointInPoly(lat, lon, polygon):
    """calcula si el punto ingresado esta dentro del polígono"""
    punto = Point(lon, lat)  # trabaja con coordenadas (x, y) que corresponden a (longitud, latitud)
    polygono_shapely = Polygon(polygon)
    return punto.within(polygono_shapely)

def SearchPolygonCountry(data):
    """Extrae la información y busca si el relámpago esta en algún polígono"""
    if PointInPoly(data['lat'], data['lon'], polygonAmericaSur):
        if PointInPoly(data['lat'], data['lon'], polygonChile):
            data['country'] = "Chile"
            return data
        elif PointInPoly(data['lat'], data['lon'], polygonUruguay):
            data['country'] = "Uruguay"
            return data
        else:
            data['country'] = "otros"
            return data
    else:
        data['country'] = False
        return data

#Funciones para moldeamiento de datos
def CalculatePulseDuration(data):
    """calcula el promedio de duración de los pulsos de un relámpago"""
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    unix_timestamps = []
    for x in data:
        ts_truncated = x[:-4] + 'Z'
        unix_timestamp = datetime.strptime(ts_truncated, date_format).timestamp()
        unix_timestamps.append(unix_timestamp)

    # Encuentra el menor y el mayor de los timestamps
    min_timestamp = min(unix_timestamps)
    max_timestamp = max(unix_timestamps)

    # Calcula la duración entre el menor y el mayor de los timestamps
    durationSeconds = max_timestamp - min_timestamp
    duration = str(timedelta(seconds=durationSeconds))
    return duration

def FiltreData(data):
    """Extrae los los pulsos anidados y genera link de google maps"""
    pulses = [pulse['time'] for pulse in data['Pulses']]
    data['duration'] = CalculatePulseDuration(pulses)
    # si el pais es otros no genera link de google maps
    if data['country'] != "otros":
        data['link'] = f"https://www.google.com/maps/search/?api=1&query={data['lat']},{data['lon']}"
        filteredData = {
            'type': data['type'],
            'time': data['time'],
            'peakCurrent': data['peakCurrent'],
            'lat': data['lat'],
            'lon': data['lon'],
            'country': data['country'],
            'duration': data['duration'],
            'link': data['link']
        }
    else:
        filteredData = {
            'type': data['type'],
            'time': data['time'],
            'peakCurrent': data['peakCurrent'],
            'lat': data['lat'],
            'lon': data['lon'],
            'country': data['country'],
            'duration': data['duration'],
        }
    return filteredData

# region prints
#datos de prueba por consola para mas información 
async def print_all(data, elapsed_time):
    """imprime todos los datos del relámpago procesados por geoCountry"""
    GCountry = GeoCountry(data['lat'], data['lon'])
    print(f"país: {GCountry}-(latitud: {data['lat']}-longitud: {data['lon']}) https://www.google.com/maps/search/?api=1&query={data['lat']},{data['lon']}")
    print("Tiempo de operación: ", elapsed_time)

async def print_v(data, elapsed_time):
    """imprime solo los datos del relámpago que están dentro de un polígono"""
    if data['country'] != False:
        print(f"país: {data['country']}-(latitud: {data['lat']}-longitud: {data['lon']}) link: {data['link']}")
        print("Tiempo de operación: ", elapsed_time)
# endregion