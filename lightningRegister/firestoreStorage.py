import asyncio
from lightningRegister.mqttFunctions import dataList
from lightningRegister.firebaseFunctions import AddDataToFirestore
from datetime import datetime
import csv

# Crea un objeto Lock que será compartido entre los dos hilos
data_lock = asyncio.Lock()

#captura tiempo actual de inicio
timeStar = int(datetime.now().timestamp())

#guarda la lista en csv de otros
def CreateCSV(dataList, country):
    with open(f'data{country}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        #Si el país es Otros, no agrega el link
        if country == "Otros":
            writer.writerow(["lat", "lon", "country", "duration", "type", "time", "peakCurrent"])
            for data in dataList:
                writer.writerow([data['lat'], data['lon'], data['country'], data['duration'], data['type'], data['time'], data['peakCurrent']])
        # Si el país es Chile o Uruguay, agrega el link
        else:
            writer.writerow(["lat", "lon", "country", "duration", "type", "time", "peakCurrent", "link"])
            for data in dataList:
                writer.writerow([data['lat'], data['lon'], data['country'], data['duration'], data['type'], data['time'], data['peakCurrent'], data['link']])

async def timerpush(time, saveCSV, saveDB, printCountry):
    """Envía los datos a Firestore cada x segundos"""
    while True:
        global timeStar
        async with data_lock: # Adquiere el lock antes de acceder a la lista
            #Si hay datos en la lista, los envía a Firestore 
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
                    if saveDB:
                        AddDataToFirestore(listChile, timeStar, timeEnd, "chile")
                    if saveCSV:
                        CreateCSV(listChile, "Chile")
                    if printCountry:
                        print(f"Chile: {len(listChile)}")
                if listUruguay:
                    if saveDB:
                        AddDataToFirestore(listUruguay, timeStar, timeEnd, "uruguay")
                    if saveCSV:
                        CreateCSV(listUruguay, "Uruguay")
                    if printCountry:
                        print(f"Uruguay: {len(listUruguay)}")
                if listOther:
                    if saveDB:
                        AddDataToFirestore(listOther, timeStar, timeEnd, "others")
                    if saveCSV:
                        CreateCSV(listOther, "Otros")
                    if printCountry:
                        print(f"Otros: {len(listOther)}")
                timeStar = timeEnd
                print(f"Total de listas: {len(dataList)}")
                dataList.clear()  # Borra la lista después de agregar los datos
        await asyncio.sleep(time)