import asyncio
import sys
import json
from asyncio_mqtt import Client
from lightningRegister.mqttFunctions import OnConnect, OnMessage
from lightningRegister.firestoreStorage import timerpush

dataSimulation = []

async def main(dataSimulation):
    async with Client(broker, port) as client:
        # Llama a la función OnConnect
        await OnConnect(client)

        # Envía los datos de simulación a través de MQTT
        for data in dataSimulation:
            # Serializa los datos en formato JSON
            payload = json.dumps(data)
            # Publica los datos en el tópico MQTT
            await client.publish("lightning", payload)

        # Llama a la función OnMessage
        await OnMessage(client)
        await asyncio.create_task(timerpush())

if __name__ == "__main__":
    # Establece las credenciales y el servidor MQTT
    broker = "test.mosquitto.org"
    port = 1883

    print("Simulando conexión al servidor MQTT...")
    print("Por favor selecciona una opción para continuar:")
    print("1 simulación en Chile")
    print("2 simulación en Brasil")
    print("3 simulación en Uruguay")
    
    while True:
        x = int(input("Ingrese la opcion: "))
        if x == 1:
            data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-33.451534,"longitude":-70.676621,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-33.815520,"longitude":-71.034497,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-39.826123,"longitude":-73.245389,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-34.9155,"lon":-71.7133}'
            dataSimulation.append(json.loads(data))
        elif x == 2:
            data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-20.845671,"longitude":-42.798012,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-22.962778,"longitude":-43.204167,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-23.550520,"longitude":-46.633309,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-21.1364,"lon":-44.3148}'
            dataSimulation.append(json.loads(data))
        elif x == 3:
            data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-33.072166,"longitude":-56.123575,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-34.905416,"longitude":-54.956322,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-34.768045,"longitude":-55.244542,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-32.5325,"lon":-55.7508}'
            dataSimulation.append(json.loads(data))
        option = input("Desea agregar mas simulaciones? (y/n): ")
        if option == "n":
            break
    
    client = Client(broker, port)
    if sys.platform == "win32":
        # Cambia al "Selector" event loop en Windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(timerpush(False))
        loop.run_until_complete(main(dataSimulation))
    except KeyboardInterrupt:
        client.disconnect()
        print("El programa fue interrumpido por el usuario. Cerrando...")
