import re
from pymongo import MongoClient
import pg8000.native

# Conexión a MongoDB (ajusta la URI según tu configuración)
client = MongoClient("mongodb://localhost:27017/")
db = client["Dataproject1"]
collection = db["estaciones_trasnporte_publico"]

# Conexión a PostgreSQL
con = pg8000.native.Connection(user="postgres", password="Welcome01", host='localhost', database='Dataproject1')

# Creamos la tabla en PostgreSQL si no existe
con.run("""
    CREATE TABLE IF NOT EXISTS estaciones_transporte_publico(
        id SERIAL PRIMARY KEY,
        transporte VARCHAR(255),
        nombre VARCHAR(255),
        cuenta VARCHAR(255)
    )
""")


# Revisamos cada documento y cogemos el value
for document in collection.find():
    transporte = document.get("transporte")
    nombre = document.get("nombre")
    cuenta = document.get("count(distinct stop_id)")
        
        # Insertamos los valores en PostgreSQL
    con.run("INSERT INTO estaciones_transporte_publico (transporte, nombre, cuenta) VALUES (:transporte, :nombre, :cuenta)", 
            transporte=transporte, nombre=nombre, cuenta=cuenta)
