import pandas as pd

from funciones.obtener_datos_api import obtener_datos_api 

apis = {
    "metro" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/transporte-barrios/records?select=coddistbar%2C%20count(distinct%20stop_id)%20as%20paradas_metro&where=transporte%3D%27metrovlc%27&group_by=coddistbar&limit=100",
}


datos_apis = {}

for nombre, url in apis.items():
    datos_apis[nombre] = obtener_datos_api(url)

# Metro
metro = datos_apis["metro"]

df_metro = pd.DataFrame([
        {
            "id": record["coddistbar"],
            "paradas_metro": record["paradas_metro"]
        }
        for record in metro["results"]
    ])