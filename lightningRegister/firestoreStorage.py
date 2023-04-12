import asyncio
from lightningRegister.mqttFunctions import dataList
from lightningRegister.firebaseFunctions import AddDataToFirestore
from datetime import datetime

# Crea un objeto Lock que será compartido entre los dos hilos
data_lock = asyncio.Lock()

#captura tiempo actual de inicio
timeStar = int(datetime.now().timestamp())

async def timerpush(test: bool = True, time: int = 300):
    """Envía los datos a Firestore cada x segundos"""
    while True:
        global timeStar
        async with data_lock: # Adquiere el lock antes de acceder a la lista
            #Si hay datos en la lista, los envía a Firestore 
            print(f"Datos en la lista: {len(dataList)}")
            if dataList:
                listChile = []
                listUruguay = []
                listOther = []
                for data in dataList:
                    if data['country'] == "Chile":
                        listChile.append(data)
                    elif data['country'] == "Uruguay":
                        listUruguay.append(data)
                    else:
                        listOther.append(data)
                timeEnd = int(datetime.now().timestamp())
                # Envía las listas por país a Firestore
                if listChile:
                    if test:
                        print(f"Chile: {len(listChile)}")
                        AddDataToFirestore(listChile, timeStar, timeEnd, "chile")
                    else:
                        print(f"Chile: {len(listChile)}")
                if listUruguay:
                    if test:
                        print(f"Uruguay: {len(listUruguay)}")
                        AddDataToFirestore(listUruguay, timeStar, timeEnd, "uruguay")
                    else:
                        print(f"Uruguay: {len(listUruguay)}")
                if listOther:
                    if test:
                        print(f"Otros: {len(listOther)}")
                        AddDataToFirestore(listOther, timeStar, timeEnd, "otros")
                timeStar = timeEnd
                dataList.clear()  # Borra la lista después de agregar los datos
        await asyncio.sleep(time)