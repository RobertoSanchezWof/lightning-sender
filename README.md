# Proyecto Lightning Sender

Este proyecto se conecta a un servidor MQTT en tiempo real para recibir datos sobre detección de rayos y determinar si un relámpago ha ocurrido dentro de una zona geográfica específica. Si se detecta un relámpago en el área, el programa añade la información del relámpago a una lista. Tras un período de tiempo establecido, el programa envía la lista de datos a Firestore, organizados por país, y luego limpia la lista para que pueda volver a llenarse. Actualmente, el programa se ejecuta en segundo plano en una Raspberry Pi utilizando una sesión de screen denominada "lightning".

## Requisitos
Este proyecto fue desarrollado en un ambiente Conda. Si deseas crear un entorno conda con las mismas dependencias del proyecto, sigue los siguientes pasos:

1. Clona el repositorio de GitHub usando SSH:

```
git clone git@github.com:RobertoSanchezWof/lightning-sender.git
```
2) Crear un nuevo entorno conda.
```
git conda create --name mi_entorno_conda
```
3) Activar el entorno conda.

```
conda activate mi_entorno_conda
```
4) Instalar los paquetes necesarios a través requirements.txt
```
pip install -r lightning-sender/requirements.txt`
```
5) Inicializar las credenciales de Firebase. Se debe tener acceso a una cuenta de Firebase y a una base de datos Firestore


## Uso

Para comenzar a utilizar el programa, sigue estos pasos:

1. Navega hasta la carpeta "lightning_sender" en tu terminal o línea de comandos.
2. Ejecuta el siguiente comando para iniciar el script:

```
screen -S lightning

```

En caso de windows  ejecutar. 
```
run.bad
```
Para ejecutar el programa de forma normal. 
```
python main.py 
```
Para ejecutar un test controlado.
```
python test.py
```  
El programa pedirá seleccionar una opción
1. Real.
2. Simulación

Real ejecutara el programa con normalidad registrando los procesos.
Simulación se conectara a un mqtt distinto y pedirá ingresar json predeterminados para corroborar las funciones del código de manera controlada. Para desconectar de la sesión sin cerrarla, presiona Ctrl + A y luego Ctrl + D.

Hay un archivo llamado config.ini que incluye variables estáticas utilizadas por el programa, junto con una descripción que acompaña a cada una de ellas para facilitar su comprensión. Antes de ejecutar el programa, por favor revise el archivo para asegurarse de que la configuración actual cumple con sus necesidades.

## Simulación
Se ha creado un test para simular casos en diferentes áreas geográficas. Para ejecutar el test, se debe correr el script test_sendData.py. Este script simula los casos de lightning en Chile, Argentina, Uruguay y fuera del cono sur, y verifica que los datos sean procesados correctamente por la función OnMessage del módulo mqttFunctions.

Para correr el test, se deben seguir los siguientes pasos:

1) Asegurarse de tener instaladas las dependencias del proyecto, descritas en el archivo requirements.txt.
2) Seleccionar la opción 2 de simulación.
3) Verificar que el test haya corrido sin errores y que los datos hayan sido procesados correctamente.

Es importante destacar que este test tiene como objetivo simular casos controlados para verificar el correcto funcionamiento de la función OnMessage, ExtractData y SearchPolygon.