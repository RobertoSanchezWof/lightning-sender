import json
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
        print("esta adentro")
        activateAddDataToFirestore = input("¿Desea activar la función addDataToFirestore()? (S/N): ")
        if activateAddDataToFirestore.upper() == "S":
            print("ingresa data a firestore")
            #AddDataToFirestore(type, latitude, longitude, time)
    else:
        print("no esta adentro")
        return False

x = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-15.551629,"longitude":-72.725977,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-15.4737,"longitude":-72.7455,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-15.607114,"longitude":-72.776314,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-15.551629,"lon":-72.725977}'

poligono = [(-70.6477450, -18.6462451), (-70.9115486, -26.3918697), (-71.6589923, -29.1521613), (-71.7469268, -30.4107818),
            (-71.7469268, -33.3947592), (-73.7183660, -37.1165262), (-73.7073193, -37.6490340), (-73.5273708, -38.1431975),
            (-73.4462883, -39.4870850), (-74.0178629, -41.0130658), (-74.5015029, -43.4369660), (-75.7909058, -46.7398606),
            (-75.7469385, -50.6250731), (-73.8123785, -54.1624340), (-67.3052219, -56.1455495), (-66.4459055, -56.0229481),
            (-66.1163595, -55.1035161), (-68.5328137, -54.8386636), (-68.5986877, -53.5794615), (-68.4451317, -52.3084786),
            (-70.0268335, -52.0660003), (-71.7123262, -52.0389766), (-72.3058844, -50.6807971), (-73.3391154, -49.9087870),
            (-72.3938190, -48.7779128), (-71.2503404, -45.3984500), (-71.5800950, -40.4302236), (-70.8106677, -38.6683561),
            (-71.0524877, -36.7036596), (-70.3050440, -36.1556178), (-69.7994204, -34.1799976), (-69.7774367, -33.4497766),
            (-70.1951258, -32.0825746), (-70.2830604, -31.0529340), (-69.8214040, -30.2211019), (-69.4777257, -28.4010648),
            (-68.3704839, -27.0786916), (-68.4364349, -25.1054974), (-68.1373059, -24.4671507), (-67.4471712, -24.2068896),
            (-66.9635312, -23.2413461), (-67.2273348, -22.7964393), (-67.8868439, -22.9381596), (-68.1946149, -21.3712444),
            (-68.4584185, -20.6533461), (-68.5903203, -20.0765701), (-68.4144512, -19.4976642), (-68.8321403, -18.9582465),
            (-69.0519767, -18.0832009), (-69.4476822, -17.5392966), (-70.5028967, -18.6254245)]

ExtractData (x,poligono)