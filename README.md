# Proyecto Lightning Sender

Este proyecto se conecta a un servidor MQTT en tiempo real para recibir datos de detección de rayos y determinar si un relámpago ha ocurrido dentro de un área geográfica específica. Si se detecta un relámpago dentro del área, el programa agrega los datos del relámpago a Firestore, una base de datos en la nube de Firebase.

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
python lightninRegister
```
