import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os import path
import random

#Extrae las credenciales alojadas en el dispositivo local
pathCredentials = path.join(path.expanduser('~'), ".auth", "wof_firebase.json")

# Inicializa la aplicación de Firebase
cred = credentials.Certificate(pathCredentials)
firebase_admin.initialize_app(cred)

# Crea una instancia de la API de Firestore
db = firestore.client()

def AddDataToFirestore(type, peakCurrent, latitude, longitude, time, country):
    """inserta los datos en la base de datos"""
    doc_id = f"{time}-{random.randint(0,9)}"
    # Crea una referencia al documento en la colección "lightning"
    doc_ref = db.collection('lightning').document(doc_id)
    # Sube la información a Firestore
    try:
        doc_ref.set({
            'type': type,
            'country': country,
            'peakCurrent': peakCurrent,
            'latitude': latitude,
            'longitude': longitude
        })
    except:
        print("Error al subir los datos a Firestore")