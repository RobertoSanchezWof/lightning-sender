from asyncio_mqtt import Client, Topic
from lightningRegister.dataExtraction import FiltreData, SearchPolygonCountry
from lightningRegister.geoCountry import GeoCountry
import sys
import time
import asyncio
import json
import csv

#timer para el control de print por consola (solo para pruebas)
timer = 0
#lista de datos almacenados en memoria
dataList = []
# Objeto Lock para sincronizar el acceso a la lista dataList
data_lock = asyncio.Lock()

# Define la función de callback para cuando se reciba un mensaje
async def OnMessage(client):
    """función que recibe los mensajes del broker"""
    async with client.messages() as messages:
        global timer
        async for message in messages:
            if Topic("lightning").matches(message.topic):
                start_time = time.time()
                #Extrae la información del JSON
                data = json.loads(message.payload.decode())
                #busca el polígono al que pertenece el relámpago y agrega country con el nombre del país
                data = SearchPolygonCountry(data)
                #si el relámpago esta dentro de un polígono, extrae la información
                if data['country'] != False:
                    #agrega duración del pulso, link de google maps y elimina data no requerida
                    data = FiltreData(data)
                    # Agrega en la lista de carácter global 
                    async with data_lock:  # Adquiere el lock antes de agregar datos a la lista
                        dataList.append(data)
                
                #calcula el tiempo de operación
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                #datos de prueba por consola para mas información 
                async def print_all():
                    """imprime todos los datos del relámpago procesados por geoCountry"""
                    GCountry = GeoCountry(data['lat'], data['lon'])
                    print(f"país: {GCountry}-(latitud: {data['lat']}-longitud: {data['lon']}) https://www.google.com/maps/search/?api=1&query={data['lat']},{data['lon']}")
                    print("Tiempo de operación: ", elapsed_time)

                async def print_v():
                    """imprime solo los datos del relámpago que están dentro de un polígono"""
                    if data['country'] != False:
                        print(f"país: {data['country']}-(latitud: {data['lat']}-longitud: {data['lon']}) link: {data['link']}")
                        print("Tiempo de operación: ", elapsed_time)
                
                #esta seccion es para mostrar data por consola de forma controlada
                if len(sys.argv) > 1:
                    """verifica si tiene argumentos para mostrar data por consola"""
                    if sys.argv[1] == "-all":
                        if len(sys.argv) > 2 and sys.argv[2].isdigit():
                            x = int(sys.argv[2])
                            if (timer + x) < time.time():
                                await print_all()
                                timer = time.time()
                        else:
                            await print_all()
                    elif sys.argv[1] == "-v":
                        if len(sys.argv) > 2 and sys.argv[2].isdigit():
                            x = int(sys.argv[2])
                            if (timer + x) < time.time():
                                await print_v()
                                timer = time.time()
                        else:
                            await print_v()
                    else:
                        print("Argumento inválido. Utilice '-all' o '-v'.")

# Establece la función de callback para cuando se conecte el cliente al broker
async def OnConnect(client):
    """función encargada de suscribirse al tópico lightning"""
    print("Conexión exitosa al servidor MQTT")
    # Suscribe el cliente al tópico "lightning"
    await client.subscribe("lightning")
