import json
from data.data import polygon
#from firebaseFunctions import addDataToFirestore

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

def ExtractData(json_string, polygon):
    """Extrae la información de un JSON y la compara con un polígono"""
    data = json.loads(json_string)
    type = data['type']
    time = data['time']
    latitude = data['lat']
    longitude = data['lon']
    print(type, latitude, longitude, time)
    if pointInPoly(latitude, longitude, polygon) == "IN":
        print("relámpago ocasionado dentro del area")
        activateAddDataToFirestore = input("¿Desea activar registrar el relámpago? (S/N): ")
        if activateAddDataToFirestore.upper() == "S":
            print("ingresa data a firestore")
            #AddDataToFirestore(type, latitude, longitude, time)
    else:
        print("relámpago no asociado al area")
        return False

x = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-15.551629,"longitude":-72.725977,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-15.4737,"longitude":-72.7455,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-15.607114,"longitude":-72.776314,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-15.551629,"lon":-72.725977}'

ExtractData (x, polygon)