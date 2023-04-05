from shapely.geometry import Point, Polygon
import constants
from datetime import datetime, timedelta

def PointInPoly(lat, lon, poligono):
    punto = Point(lon, lat)  # trabaja con coordenadas (x, y) que corresponden a (longitud, latitud)
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
    duration = str(timedelta(seconds=durationSeconds))
    return duration

def FiltreData(data):
    """Extrae los los pulsos anidados y genera link de google maps"""
    pulses = [pulse['time'] for pulse in data['Pulses']]
    data['duration'] = CalculatePulseDuration(pulses)
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
    return filteredData

def SearchPolygonCountry(data):
    """Extrae la información y busca si el relámpago esta en algún polígono"""
    if PointInPoly(data['lat'], data['lon'], constants.polygonAmericaSur) == True:
        if PointInPoly(data['lat'], data['lon'], constants.polygonChile) == True:
            data['country'] = "Chile"
            return data
        elif PointInPoly(data['lat'], data['lon'], constants.polygonUruguay) == True:
            data['country'] = "Uruguay"
            return data
        elif PointInPoly(data['lat'], data['lon'], constants.polygonBrasil) == True:
            data['country'] = "Brasil"
            return data
        else:
            data['country'] = False
            return data
    else:
        data['country'] = False
        return data