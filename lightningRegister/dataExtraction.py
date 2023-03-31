from shapely.geometry import Point, Polygon
import json
import constants
from datetime import datetime, timedelta
#from testDataExtraction import GeoCountry

def PointInPoly(lat, lon, poligono):
    punto = Point(lon, lat)  # Shapely trabaja con coordenadas (x, y) que corresponden a (longitud, latitud)
    poligono_shapely = Polygon(poligono)
    return punto.within(poligono_shapely)

def CalculatePulseDuration(data):
    """calcula el promedio de duración de los pulsos de un relampago"""
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
    duration = timedelta(seconds=durationSeconds)
    return duration

def ExtractData(json_string):
    """Extrae la información de un JSON y la compara con un polígono"""
    data = json.loads(json_string)
    type = data['type']
    time = data['time']
    peakCurrent = data['peakCurrent']
    latitude = data['lat']
    longitude = data['lon']
    pulses = [pulse["time"] for pulse in data["Pulses"]]
    duration = CalculatePulseDuration(pulses)
    return type, peakCurrent, latitude, longitude, time, duration

def SearchPolygon(latitude, longitude):
    """Busca si el relámpago esta en algún polígono"""
    if PointInPoly(latitude, longitude, constants.polygonAmericaSur) == True:
        if PointInPoly(latitude, longitude, constants.polygonChile) == True:
            area = "Chile"
            return area
        elif PointInPoly(latitude, longitude, constants.polygonBrasil) == True:
            area = "Brasil"
            return area
        elif PointInPoly(latitude, longitude, constants.polygonUruguay) == True:
            area = "Uruguay"
            return area
        else:
            return False
    else:
        return False