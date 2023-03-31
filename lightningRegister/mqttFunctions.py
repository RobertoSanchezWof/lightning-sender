from asyncio_mqtt import Client, Topic
from firebaseFunctions import AddDataToFirestore
from dataExtraction import ExtractData, SearchPolygon
from geoCountry import GeoCountry
import sys
import time
import asyncio

# Define la función de callback para cuando se reciba un mensaje
async def OnMessage(client):
    await client.subscribe("lightning")
    async with client.messages() as messages:
        async for message in messages:
            if Topic("lightning").matches(message.topic):
                start_time = time.time()
            
                type, peakCurrent, latitude, longitude, timeEvent, duration = ExtractData(message.payload.decode())
                
                #busca el polígono al que pertenece el relámpago
                country = SearchPolygon(latitude, longitude)
                link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
                
                #si el relámpago esta dentro de un polígono, lo sube a la base de datos
                if country != False:
                    print("registra")
                #     AddDataToFirestore(type, peakCurrent, latitude, longitude, timeEvent, country, link, duration)

                end_time = time.time()
                elapsed_time = end_time - start_time
                #datos de prueba por consola para mas información 
                
                async def print_all():
                    GCountry = GeoCountry(latitude, longitude)
                    print(f"país: {GCountry} - (latitud: {latitude} - longitud: {longitude}) link: {link}")
                    print("Tiempo de operación: ", elapsed_time)

                async def print_v():
                    if country != False:
                        print(f"país: {country} - (latitud: {latitude} - longitud: {longitude}) link: {link}")
                        print("Tiempo de operación: ", elapsed_time)
                
                #esta seccion es para mostrar data por consola de forma controlada
                if len(sys.argv) > 1:
                    if sys.argv[1] == "-all":
                        if len(sys.argv) > 2 and sys.argv[2].isdigit():
                            x = int(sys.argv[2])
                            await print_all()
                            await asyncio.sleep(x)
                        else:
                            await print_all()
                    elif sys.argv[1] == "-v":
                        if len(sys.argv) > 2 and sys.argv[2].isdigit():
                            x = int(sys.argv[2])
                            await print_v()
                            await asyncio.sleep(x)
                        else:
                            await print_v()
                    else:
                        print("Argumento inválido. Utilice '-all' o '-v'.")

# Establece la función de callback para cuando se conecte el cliente al broker
async def OnConnect(client):
    print("Conexión exitosa al servidor MQTT")
    # Suscribe el cliente al tópico "lightning"
    await client.subscribe("lightning")
