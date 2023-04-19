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
run.bat
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

## Proceso interno de funcionamiento

1. Inicialmente, el programa importa todas las librerías y módulos necesarios, así como también lee y valida la configuración de un archivo 'config.ini'.
2. Se conecta a un servidor MQTT y se suscribe al tópico "lightning" para recibir información sobre rayos.
3. Cada vez que se recibe un mensaje del tópico "lightning", se procesa y se guarda en una lista. Esto incluye filtrar los datos, calcular la duración de los pulsos y verificar si el rayo está dentro de un polígono específico (Chile, Uruguay u otros).
4. Periódicamente, según el tiempo especificado en la configuración, el programa guarda los datos almacenados en la lista de acuerdo a las siguientes opciones:
    * Guardar en una base de datos de Firestore.  
    * Guardar en un archivo CSV.
    * Imprimir la cantidad de datos por país en la consola.
5. Después de guardar los datos, la lista se vacía y el proceso continúa desde el paso 3.

El código también incluye funciones para manejar conexiones y mensajes MQTT, así como funciones para trabajar con la base de datos Firestore y archivos CSV. En general, el programa se encarga de recibir información sobre rayos, procesarla y almacenarla de manera organizada según las preferencias del usuario.

## Diagrama de flujo

https://drive.google.com/file/d/1agI55qU_g0tX1vC2JyIL8KrezY0d1Zzn/view?usp=share_link
