import paho.mqtt.client as mqtt
from mqttFunctions import OnConnect, OnMessage

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