import asyncio
import sys
from asyncio_mqtt import Client
from lightningRegister.mqttFunctions import OnConnect, OnMessage
from lightningRegister.firestoreStorage import timerpush

async def main():
    """Función principal que itera el bucle de eventos"""
    async with Client(broker, port) as client:
        # Llama a la función OnConnect
        await OnConnect(client)

        # Llama a la función OnMessage
        await OnMessage(client)
        await asyncio.create_task(timerpush())

if __name__ == "__main__":
    """función principal"""
    # Establece las credenciales y el servidor MQTT
    broker = "Test.dtect.africa"
    port = 1883

    client = Client(broker, port)
    if sys.platform == "win32":
        # Cambia al "Selector" event loop en Windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(timerpush())
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        client.disconnect()
        print("El programa fue interrumpido por el usuario. Cerrando...")