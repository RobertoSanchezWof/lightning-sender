import asyncio
import sys
from asyncio_mqtt import Client
from lightningRegister.mqttFunctions import OnConnect, OnMessage
from lightningRegister.firestoreStorage import timerpush
import configparser
from configparser import NoSectionError, NoOptionError
import logging

# Configura el archivo de registro
logging.basicConfig(filename='error.txt', level=logging.ERROR)

# Accede a los valores de configuración
config = configparser.ConfigParser()
config.read('config.ini')

try:
    time = config.getint('general', 'TIME')
    saveDB = config.getboolean('general', 'SAVE_DB')
    saveCSV = config.getboolean('general', 'SAVE_CSV')
    printCountry = config.getboolean('general', 'PRINT_CUNTRY')
    printInfo = config.getboolean('info', 'PRINT_INFO')
    timeInfo = config.getint('info', 'TIME_INFO')
    typeInfo = config.get('info', 'TYPE_INFO')
except NoSectionError:
    print("Error: No se encuentra la sección en el archivo de configuración.")
except NoOptionError:
    print("Error: No se encuentra la opción en el archivo de configuración.")
except ValueError:
    print("Error: Valor incorrecto en el archivo de configuración.")

# Función principal
async def main(printInfo, timeInfo, typeInfo):
    """Función principal que itera el bucle de eventos"""
    async with Client(broker, port) as client:
        # Llama a la función OnConnect
        await OnConnect(client)

        # Llama a la función OnMessage
        await OnMessage(client, printInfo, timeInfo, typeInfo)
        await asyncio.create_task(timerpush())

if __name__ == "__main__":
    """función principal"""
    # Establece las credenciales y el servidor MQTT
    broker = "Test.dtect.africa"
    port = 1883

    client = Client(broker, port)
    if sys.platform == "win32":
        # Cambia al "Selector" event loop en Windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    timerpush_task = None
    
    while True:
        try:
            timerpush_task = loop.create_task(timerpush(time, saveCSV, saveDB, printCountry))
            loop.run_until_complete(main(printInfo, timeInfo, typeInfo))
        except KeyboardInterrupt as e:
            client.disconnect()
            print("El programa fue interrumpido por el usuario. Cerrando...")
            break
        except Exception as e:  # Registra cualquier evento de interrupción y continua el bucle
            logging.error(f"Se produjo una excepción: {e}")
            if timerpush_task:  # Cancela la tarea timerpush si está ejecutándose
                timerpush_task.cancel()
            loop.stop()  # Detén el bucle de eventos actual
            loop = asyncio.new_event_loop()  # Crea un nuevo bucle de eventos
            asyncio.set_event_loop(loop)  # Establece el nuevo bucle de eventos
            continue  # Continúa el bucle para reiniciar los hilos
