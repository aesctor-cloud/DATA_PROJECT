import re
from pymongo import MongoClient
import pg8000.native

# Conexión a MongoDB (ajusta la URI según tu configuración)
client = MongoClient("mongodb://localhost:27017/")
db = client["Dataproject1"]
collection = db["esperanza_vida"]

# Conexión a PostgreSQL
con = pg8000.native.Connection(user="postgres", password="Welcome01", host='localhost', database='Dataproject1')

# Creamos la tabla en PostgreSQL si no existe
con.run("""
    CREATE TABLE IF NOT EXISTS esperanza_vida(
        distrito VARCHAR(255) PRIMARY KEY,
        valor VARCHAR(255)
    )
""")


# Revisamos cada documento y cogemos el value
for document in collection.find():
    distrito = document.get("distrito")
    valor = document.get("valor")
        
        # Insertamos los valores en PostgreSQL
    con.run("INSERT INTO esperanza_vida (distrito, valor) VALUES (:distrito, :valor)", 
            distrito=distrito, valor=valor)
