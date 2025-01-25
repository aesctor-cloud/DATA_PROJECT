import pandas as pd

from funciones.obtener_datos_api import obtener_datos_api 

apis = {
    "geo" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/barris-barrios/records?order_by=nombre&limit=100"
}


datos_apis = {}

for nombre, url in apis.items():
    datos_apis[nombre] = obtener_datos_api(url)

# Geo
geo = datos_apis["geo"]

df_geo = pd.DataFrame([
        {
            "id": record["coddistbar"],
            "barrio": record["nombre"],
            # "geometry": record["geo_shape"]["geometry"],
            # "lat": record["geo_point_2d"]["lat"],
            # "lon": record["geo_point_2d"]["lon"]
        }
        for record in geo["results"]
    ])