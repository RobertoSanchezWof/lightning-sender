import asyncio
import mqttFunctions
from firebaseFunctions import AddDataToFirestore
from datetime import datetime

# Crea un objeto Lock que será compartido entre los dos hilos
data_lock = asyncio.Lock()

#captura tiempo actual de inicio
timeStar = int(datetime.now().timestamp())

async def funcion():
    while True:
        global timeStar
        async with data_lock: # Adquiere el lock antes de acceder a la lista
        # Aquí va el código de la función que quieres ejecutar en segundo plano
            if mqttFunctions.dataList:
                timeEnd = int(datetime.now().timestamp())
                AddDataToFirestore(mqttFunctions.dataList, timeStar, timeEnd)
                timeStar = timeEnd
                mqttFunctions.dataList.clear()  # Borra la lista después de agregar los datos
        await asyncio.sleep(300)  # espera 5 segundos antes de ejecutar la función nuevamente
