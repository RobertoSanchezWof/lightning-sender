import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os import path

#Extrae las credenciales alojadas en el dispositivo local
pathCredentials = path.join(path.expanduser('~'), ".auth", "wof_firebase.json")

# Inicializa la aplicación de Firebase
cred = credentials.Certificate(pathCredentials)
firebase_admin.initialize_app(cred)

# Crea una instancia de la API de Firestore
db : firestore.firestore.Client = firestore.client()

def AddDataToFirestore(data, dateStart, dateEnd):
    """inserta los datos en la base de datos"""
    # Crea una referencia al documento en la colección "lightning"
    doc_ref = db.collection('testing/lightning/america').document(str(dateEnd))
    # Sube la información a Firestore
    try:
        doc_ref.set({
            'timeStart': dateStart,
            'timeEnd': dateEnd,
            'data': data
        })
    except Exception as e:
        print("Error al subir los datos a Firestore:", e)