import pandas as pd

from funciones.obtener_datos_api import obtener_datos_api 

apis = {
    "vulnerabilidad" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/vulnerabilidad-por-barrios/records?select=codbar%2C%20avg(ind_global)%20as%20vulnerabilildad&group_by=codbar&limit=100"
}


datos_apis = {}

for nombre, url in apis.items():
    datos_apis[nombre] = obtener_datos_api(url)

# Vulnerabilidad
vulne = datos_apis["vulnerabilidad"]

df_vulne = pd.DataFrame([
        {
            "id": record["codbar"],
            "vulne": record["vulnerabilildad"]
        }
        for record in vulne["results"]
    ])
