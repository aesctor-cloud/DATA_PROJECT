import pandas as pd

from funciones.obtener_datos_api import obtener_datos_api 

apis = {
    "alquiler" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/precio-alquiler-vivienda/records?select=codbar_coddistrit%2C%20avg(precio_2022_euros_m2)%20as%20precio_alquiler_m2&group_by=codbar_coddistrit&limit=100",
}


datos_apis = {}

for nombre, url in apis.items():
    datos_apis[nombre] = obtener_datos_api(url)


# Alquiler
alquiler = datos_apis["alquiler"]

df_alquiler = pd.DataFrame([
        {
            "id": record["codbar_coddistrit"],
            "precio_alquiler": record["precio_alquiler_m2"]
        }
        for record in alquiler["results"]
    ])