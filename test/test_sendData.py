import random
from dataExtraction import ExtractData, SearchPolygon

print("Ejecutando prueba controlada de lightning send")
print("Por favor seleccione el tipo de simulación que desea realizar:")
print(" 1 = Chile\n 2 = Argentina\n 3 = Uruguay\n 4 = Brasil\n 5 = Fuera de zona")
area = input("Ingrese el número de la simulación que desea realizar: ")

data = ""

if area == "1":
    data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-15.551629,"longitude":-72.725977,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-15.4737,"longitude":-72.7455,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-15.607114,"longitude":-72.776314,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-73.3443162,"lon":-37.4857560}'
elif area =="2":
    data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-15.551629,"longitude":-72.725977,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-15.4737,"longitude":-72.7455,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-15.607114,"longitude":-72.776314,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-62.7450008,"lon":-27.9361806}'
elif area == "3":
    data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-15.551629,"longitude":-72.725977,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-15.4737,"longitude":-72.7455,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-15.607114,"longitude":-72.776314,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-57.2759506,"lon":-32.4170663}'
elif area == "4":
    data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-15.551629,"longitude":-72.725977,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-15.4737,"longitude":-72.7455,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-15.607114,"longitude":-72.776314,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-56.0068403,"lon":-1.4061088}'
elif area == "5":
    data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-15.551629,"longitude":-72.725977,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-15.4737,"longitude":-72.7455,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-15.607114,"longitude":-72.776314,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":138.4103847,"lon":-25.7998912}'
else:
    print("Opción no válida")
    exit()

def OnMessage(client, userdata, message):
    #print(f"Mensaje recibido en el tópico {message.topic}:  otro mensaje {message.payload.decode()}")
    type, peakCurrent, latitude, longitude, time = ExtractData(message)
    #busca el polígono al que pertenece el relámpago
    country = SearchPolygon(latitude, longitude)
    #si el relámpago esta dentro de un polígono, lo sube a la base de datos
    if country != False:
        time = f"{time}-{random.randint(0,9)}"
        print("estos serian los datos a almacenar en Firestore: ")
        print(f"ID: {time}")
        print(f"  Tipo: {type}\n  peakCurrent: {peakCurrent}\n  latitude: {latitude}\n  longitude: {longitude}\n  country: {country}")
    #   AddDataToFirestore(type, peakCurrent, latitude, longitude, time, country)
    else:
        print("Las coordenadas (138.4103847,-25.7998912) no se encuentra dentro de un polígono")

OnMessage(None, None, data)



