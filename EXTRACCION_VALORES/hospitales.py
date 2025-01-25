import pandas as pd

from funciones.obtener_datos_api import obtener_datos_api 

apis = {
    "hospitales" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/hospitales/records?select=coddistbar%2C%20count(distinct%20nombre)%20as%20hospitales&where=tipo%3D%22Hospital%22&group_by=coddistbar&limit=100"
}


datos_apis = {}

for nombre, url in apis.items():
    datos_apis[nombre] = obtener_datos_api(url)

# Hospitales
hospi = datos_apis["hospitales"]

df_hospi = pd.DataFrame([
        {
            "id": record["coddistbar"],
            "hospitales": record["hospitales"]
        }
        for record in hospi["results"]
    ])