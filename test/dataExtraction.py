import json
import constants

# Improved point in polygon test which includes edge
# and vertex points

def pointInPoly(x,y,poly):

    # check if point is a vertex
    if (x,y) in poly: return "IN"

    # check if point is on a boundary
    for i in range(len(poly)):
        p1 = None
        p2 = None
        if i==0:
            p1 = poly[0]
            p2 = poly[1]
        else:
            p1 = poly[i-1]
            p2 = poly[i]
        if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
            return "IN"
    
    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    if inside: return "IN"
    else: return "OUT"

def ExtractData(json_string):
    """Extrae la información de un JSON y la compara con un polígono"""
    data = json.loads(json_string)
    type = data['type']
    time = data['time']
    peakCurrent = data['peakCurrent']
    latitude = data['lat']
    longitude = data['lon']
    return type, peakCurrent, latitude, longitude, time

def SearchPolygon(latitude, longitude):
    """Busca si el relámpago esta en algún polígono"""
    result = pointInPoly(latitude, longitude, constants.polygonAmericaSur)
    if result == "IN":
        if pointInPoly(latitude, longitude, constants.polygonChile) == "IN":
            return "Chile"
        elif pointInPoly(latitude, longitude, constants.polygonBrasil) == "IN": 
            return "Brasil"
        elif pointInPoly(latitude, longitude, constants.polygonArgentinaUruguay) == "IN" and pointInPoly(latitude, longitude, constants.polygonUruguay) == "OUT":
            return "Argentina"
        elif pointInPoly(latitude, longitude, constants.polygonUruguay) == "IN":
            return "Uruguay"
    else:
        return False