import pandas as pd

from funciones.obtener_datos_api import obtener_datos_api 

apis = {
    "compra" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/precio-de-compra-en-idealista/records?select=coddistbar%2C%20avg(precio_2022_euros_m2)%20as%20precio_compra_m2&group_by=coddistbar&limit=100"
}


datos_apis = {}

for nombre, url in apis.items():
    datos_apis[nombre] = obtener_datos_api(url)

# Compra
compra = datos_apis["compra"]

df_compra = pd.DataFrame([
        {
            "id": record["coddistbar"],
            "precio_compra": record["precio_compra_m2"]
        }
        for record in compra["results"]
    ])
