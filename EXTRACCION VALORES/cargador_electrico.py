import re
from pymongo import MongoClient
import pg8000.native

# Conexión a MongoDB (ajusta la URI según tu configuración)
client = MongoClient("mongodb://localhost:27017/")
db = client["Dataproject1"]
collection = db["cargador_electrico"]

# Conexión a PostgreSQL
con = pg8000.native.Connection(user="postgres", password="Welcome01", host='localhost', database='Dataproject1')

# Creamos la tabla en PostgreSQL si no existe
con.run("""
    CREATE TABLE IF NOT EXISTS cargador_electrico(
        coddistbar VARCHAR(255) PRIMARY KEY,
        lon VARCHAR(255),
        lat VARCHAR(255)
    )
""")


# Revisamos cada documento y cogemos el value
for document in collection.find():
    coddistbar = document.get("coddistbar")
    lon = document.get("lon")
    lat = document.get("lat")
        
        # Insertamos los valores en PostgreSQL
    con.run("INSERT INTO cargador_electrico (codistbar, lon, lat) VALUES (:coddistbar, :lon, :lat)", 
            coddistbar=coddistbar, lon=lon, lat=lat)
