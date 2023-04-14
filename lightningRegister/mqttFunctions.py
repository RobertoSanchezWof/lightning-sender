from asyncio_mqtt import Client, Topic
from lightningRegister.dataExtraction import FiltreData, SearchPolygonCountry, print_all, print_v
import time
import asyncio
import json

#timer para el control de print por consola (solo para pruebas)
timer = 0
#lista de datos almacenados en memoria
dataList = []
# Objeto Lock para sincronizar el acceso a la lista dataList
data_lock = asyncio.Lock()

# Define la función de callback para cuando se reciba un mensaje
async def OnMessage(client, printInfo, timeInfo, typeInfo = None):
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

                #Esta seccion es para mostrar data por consola de forma controlada
                if printInfo:
                    """verifica si tiene argumentos para mostrar data por consola"""
                    if typeInfo == "all":
                        # Suma el timer mas el tiempo de espera  y verifica que sea menor al tiempo actual para entrar
                        if (timer + timeInfo) < time.time():
                            await print_all(data, elapsed_time)
                            timer = time.time()
                    elif typeInfo == "v":
                        if (timer + timeInfo) < time.time():
                            await print_v(data, elapsed_time)
                            timer = time.time()
                    else:
                        print("Argumento inválido. Utilice 'all' o 'v'.")

# Establece la función de callback para cuando se conecte el cliente al broker
async def OnConnect(client):
    """función encargada de suscribirse al tópico lightning"""
    print("Conexión exitosa al servidor MQTT")
    # Suscribe el cliente al tópico "lightning"
    await client.subscribe("lightning")
