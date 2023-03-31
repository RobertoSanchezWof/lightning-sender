import asyncio
from asyncio_mqtt import Client
from mqttFunctions import OnConnect, OnMessage

async def main():
    # Establece las credenciales y el servidor MQTT
    broker = "Test.dtect.africa"
    port = 1883
    
    async with Client(broker, port) as client:
        # Llama a la función OnConnect
        await OnConnect(client)

        # Llama a la función OnMessage
        await OnMessage(client)

if __name__ == "__main__":
    # Cambia al "Selector" event loop en Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("El programa fue interrumpido por el usuario. Cerrando...")
