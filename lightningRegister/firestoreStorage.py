import asyncio
from lightningRegister.mqttFunctions import dataList
from lightningRegister.firebaseFunctions import AddDataToFirestore
from datetime import datetime

# Crea un objeto Lock que será compartido entre los dos hilos
data_lock = asyncio.Lock()

#captura tiempo actual de inicio
timeStar = int(datetime.now().timestamp())

async def timerpush(test: bool = True):
    """Envía los datos a Firestore cada x segundos"""
    while True:
        global timeStar
        async with data_lock: # Adquiere el lock antes de acceder a la lista
            #Si hay datos en la lista, los envía a Firestore 
            print(f"Datos en la lista: {len(dataList)}")
            if dataList:
                listBrasil = []
                listChile = []
                listUruguay = []
                for data in dataList:
                    if data['country'] == "Brasil":
                        listBrasil.append(data)
                    elif data['country'] == "Chile":
                        listChile.append(data)
                    elif data['country'] == "Uruguay":
                        listUruguay.append(data)
                timeEnd = int(datetime.now().timestamp())
                # Envía las listas por país a Firestore
                if listBrasil:
                    if test:
                        #print(f"Brasil: {len(listBrasil)}")
                        AddDataToFirestore(listBrasil, timeStar, timeEnd, "brasil")
                if listChile:
                    if test:
                        #print(f"Chile: {len(listChile)}")
                        AddDataToFirestore(listChile, timeStar, timeEnd, "chile")
                if listUruguay:
                    if test:
                        #print(f"Uruguay: {len(listUruguay)}")
                        AddDataToFirestore(listUruguay, timeStar, timeEnd, "uruguay")
                timeStar = timeEnd
                dataList.clear()  # Borra la lista después de agregar los datos
        await asyncio.sleep(300)