from pymongo import MongoClient


# Conexión a MongoDB
def obtener_mongo(collection_name):
    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client["Dataproject1"]
    collection = db[collection_name]

    # Obtener todos los documentos de la colección
    documentos = collection.find()

    for documento in documentos:
            print(documento)

# Llamada a la función obtener_mongo con la colección 'geo'
obtener_mongo("geo")