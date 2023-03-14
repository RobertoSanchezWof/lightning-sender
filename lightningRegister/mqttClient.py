import paho.mqtt.client as mqtt
from dataExtraction import ExtractData
import constants

# Define la función de callback para cuando se reciba un mensaje
def OnMessage(client, userdata, message):
    #print(f"Mensaje recibido en el tópico {message.topic}:  otro mensaje {message.payload.decode()}")
    ExtractData(message.payload.decode(), constants.polygon)

# Establece la función de callback para cuando se conecte el cliente al broker
def OnConnect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al servidor MQTT")
        # Suscribe el cliente al tópico "lightning"
        client.subscribe("lightning")
    else:
        print("Error al conectarse al servidor MQTT")

# Crea una instancia del cliente MQTT
client = mqtt.Client()
# Asigna las funciones de callback al cliente MQTT
client.on_connect = OnConnect
client.on_message = OnMessage

# Conecta el cliente MQTT al servidor y puerto especificados
client.connect("Test.dtect.africa", 1883)

# Inicia el bucle infinito del cliente MQTT para mantener la conexión activa
client.loop_forever()
