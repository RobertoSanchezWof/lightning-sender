import paho.mqtt.client as mqtt
from firebaseFunctions import AddDataToFirestore
from dataExtraction import ExtractData, SearchPolygon
import sys
import time

# Define la función de callback para cuando se reciba un mensaje
def OnMessage(client, userdata, message):
    start_time = time.time()
    #print(f"Mensaje recibido en el tópico {message.topic}:  otro mensaje {message.payload.decode()}")
    type, peakCurrent, latitude, longitude, timeEvent = ExtractData(message.payload.decode())
    #busca el polígono al que pertenece el relámpago
    country = SearchPolygon(latitude, longitude)
    #si el relámpago esta dentro de un polígono, lo sube a la base de datos
    if country != False:
        AddDataToFirestore(type, peakCurrent, latitude, longitude, timeEvent, country)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Tiempo de ejecución: {elapsed_time:.5f} segundos")  
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        print("Tipo de relámpago: ", type)
        print("Corriente pico: ", peakCurrent)
        print("Latitud: ", latitude)
        print("Longitud: ", longitude)
        print("Tiempo: ", timeEvent)
        if country == False:
            print("País: ", "Fuera de Area" )

# Establece la función de callback para cuando se conecte el cliente al broker
def OnConnect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al servidor MQTT")
        # Suscribe el cliente al tópico "lightning"
        client.subscribe("lightning")
    else:
        print("Error al conectarse al servidor MQTT")