import asyncio
import mqttFunctions
from firebaseFunctions import AddDataToFirestore
from datetime import datetime

# Crea un objeto Lock que será compartido entre los dos hilos
data_lock = asyncio.Lock()

#captura tiempo actual de inicio
timeStar = int(datetime.now().timestamp())

async def timerpush():
    while True:
        global timeStar
        async with data_lock: # Adquiere el lock antes de acceder a la lista
            #Si hay datos en la lista, los envía a Firestore 
            if mqttFunctions.dataList:
                listBrasil = []
                listChile = []
                listUruguay = []
                for data in mqttFunctions.dataList:
                    if data['country'] == "Brasil":
                        listBrasil.append(data)
                    elif data['country'] == "Chile":
                        listChile.append(data)
                    elif data['country'] == "Uruguay":
                        listUruguay.append(data)
                timeEnd = int(datetime.now().timestamp())
                # Envía las listas por país a Firestore
                if listBrasil:
                    AddDataToFirestore(listBrasil, timeStar, timeEnd, "brasil")
                if listChile:
                    AddDataToFirestore(listChile, timeStar, timeEnd, "chile")
                if listUruguay:
                    AddDataToFirestore(listUruguay, timeStar, timeEnd, "uruguay")
                timeStar = timeEnd
                mqttFunctions.dataList.clear()  # Borra la lista después de agregar los datos
        await asyncio.sleep(300)  # espera 5 segundos antes de ejecutar la función nuevamente