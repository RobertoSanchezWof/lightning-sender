import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random

# Inicializa la aplicación de Firebase
cred = credentials.Certificate('./credenciales')
firebase_admin.initialize_app(cred)

# Crea una instancia de la API de Firestore
db = firestore.client()

def AddDataToFirestore(type, latitude, longitude, time):
    """inserta los datos en la base de datos"""
    doc_id = f"{time}-{random.randint(0, 100000)}"
    # Crea una referencia al documento en la colección "lightning"
    doc_ref = db.collection('lightning').document(doc_id)
    # Sube la información a Firestore
    try:
        doc_ref.set({
            'type': type,
            'latitude': latitude,
            'longitude': longitude
        })
    except:
        print("Error al subir los datos a Firestore")