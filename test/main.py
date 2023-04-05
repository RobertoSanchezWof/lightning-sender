from asyncio_mqtt import Client, Topic
from dataExtraction import FiltreData, SearchPolygonCountry
from geoCountry import GeoCountry
from firestoreStorage import timerpush
import sys
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
def OnMessage(client):
    global timer, dataList
    #Extrae la información del JSON
    data = json.loads(client)
    #busca el polígono al que pertenece el relámpago y agrega country con el nombre del país
    data = SearchPolygonCountry(data)
    #si el relámpago esta dentro de un polígono, extrae la información
    if data['country'] != False:
        #agrega duración del pulso y link de google maps
        data = FiltreData(data)
        # Agrega en la lista de carácter global 
        dataList.append(data)

if __name__ == "__main__":
    
    print("Bienvenido a la simulación de LightningRegister")
    print("Porfavor selecciona una opcion para continuar:")
    print("1 simulacion en Chile")
    print("2 simulacion en Brasil")
    print("3 simulacion en Uruguay")
    
    while True:
        x = int(input("Ingrese la opcion: "))
        if x == 1:
            data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-33.451534,"longitude":-70.676621,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-33.815520,"longitude":-71.034497,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-39.826123,"longitude":-73.245389,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-34.9155,"lon":-71.7133}'
            OnMessage(data)
        elif x == 2:
            data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-20.845671,"longitude":-42.798012,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-22.962778,"longitude":-43.204167,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-23.550520,"longitude":-46.633309,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-21.1364,"lon":-44.3148}'
            OnMessage(data)
        elif x == 3:
            data = '{"type":0,"time":1678292764430,"peakCurrent":-8963,"numSensors":10,"icHeight":0,"icMultiplicity":0,"cgMultiplicity":3,"Pulses":[{"type":0,"time":"2023-03-08T16:25:50.766793518Z","latitude":-33.072166,"longitude":-56.123575,"peakCurrent":-8963,"numSensors":10,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.696567000Z","latitude":-34.905416,"longitude":-54.956322,"peakCurrent":1247,"numSensors":7,"icHeight":0},{"type":0,"time":"2023-03-08T16:25:50.651452872Z","latitude":-34.768045,"longitude":-55.244542,"peakCurrent":8195,"numSensors":8,"icHeight":0}],"lat":-32.5325,"lon":-55.7508}'
            OnMessage(data)
        option = input("Desea agregar mas simulaciones? (y/n): ")
        if option == "n":
            break
    #print(dataList)
    timerpush(dataList)
