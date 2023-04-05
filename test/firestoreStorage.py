import asyncio
#from firebaseFunctions import AddDataToFirestore
from datetime import datetime

# Crea un objeto Lock que será compartido entre los dos hilos
#data_lock = asyncio.Lock()

#captura tiempo actual de inicio
timeStar = int(datetime.now().timestamp())
count = 0

def timerpush(dataList):
    global timeStar, count
    print("Datos en memoria:", len(dataList))
    if dataList: # Adquiere el lock antes de acceder a la lista
        #Si hay datos en la lista, los envía a Firestore 
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
            print("Enviando datos a Firestore")
            print("Tiempo de inicio:", timeStar)
            print("Tiempo de fin:", timeEnd)
            if listBrasil:
                print(f"Brasil: {len(listBrasil)}")
                #AddDataToFirestore(listBrasil, timeStar, timeEnd, "brasil")
            if listChile:
                print(f"Chile: {len(listChile)}")
                #AddDataToFirestore(listChile, timeStar, timeEnd, "chile")
            if listUruguay:
                print(f"Uruguay: {len(listUruguay)}")
                #AddDataToFirestore(listUruguay, timeStar, timeEnd, "uruguay")
            timeStar = timeEnd
            dataList.clear()  # Borra la lista después de agregar los datos