import paho.mqtt.client as mqtt
from firebaseFunctions import AddDataToFirestore
from dataExtraction import ExtractData, SearchPolygon

# Define la función de callback para cuando se reciba un mensaje
def OnMessage(client, userdata, message):
    #print(f"Mensaje recibido en el tópico {message.topic}:  otro mensaje {message.payload.decode()}")
    type, peakCurrent, latitude, longitude, time = ExtractData(message.payload.decode())
    #busca el polígono al que pertenece el relámpago
    country = SearchPolygon(latitude, longitude)
    #si el relámpago esta dentro de un polígono, lo sube a la base de datos
    if country != False:
        print(type, peakCurrent, latitude, longitude, time, country)
        AddDataToFirestore(type, peakCurrent, latitude, longitude, time, country)
    else:
        print("relámpago no asociado al area")
    

# Establece la función de callback para cuando se conecte el cliente al broker
def OnConnect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al servidor MQTT")
        # Suscribe el cliente al tópico "lightning"
        client.subscribe("lightning")
    else:
        print("Error al conectarse al servidor MQTT")

def main():
    # Crea una instancia del cliente MQTT
    client = mqtt.Client()
    # Asigna las funciones de callback al cliente MQTT
    client.on_connect = OnConnect
    client.on_message = OnMessage

    # Conecta el cliente MQTT al servidor y puerto especificados
    client.connect("Test.dtect.africa", 1883)

    # Inicia el bucle infinito del cliente MQTT para mantener la conexión activa
    client.loop_forever()

if __name__ == "__main__":
    main()

# x = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-15.551629,"longitude":-72.725977,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-15.4737,"longitude":-72.7455,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-15.607114,"longitude":-72.776314,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-72.3100132,"lon":-37.3876175}'
# x2 = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-15.551629,"longitude":-72.725977,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-15.4737,"longitude":-72.7455,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-15.607114,"longitude":-72.776314,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-15.551629,"lon":-72.725977}'

# OnMessage(None, None, x2)