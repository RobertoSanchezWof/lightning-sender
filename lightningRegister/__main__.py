import asyncio
from asyncio_mqtt import Client
from mqttFunctions import OnConnect, OnMessage
from funcion import funcion

async def main():
    async with Client(broker, port) as client:
        # Llama a la función OnConnect
        await OnConnect(client)

        # Llama a la función OnMessage
        await OnMessage(client)
        await asyncio.create_task(funcion())

if __name__ == "__main__":
    # Establece las credenciales y el servidor MQTT
    broker = "Test.dtect.africa"
    port = 1883

    client = Client(broker, port)
    # Cambia al "Selector" event loop en Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(funcion())
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        client.disconnect()
        print("El programa fue interrumpido por el usuario. Cerrando...")