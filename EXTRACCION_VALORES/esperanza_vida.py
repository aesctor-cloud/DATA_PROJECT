import pandas as pd

from funciones.normalizar_nombre_barrio import normalizar_nombre_barrio
from funciones.obtener_datos_api import obtener_datos_api
from geo import df_geo 

# URLs de las APIs
apis = {
    "esperanza_vida"="https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/oe_28_esperanza_vida/records?select=distrito%2C%20valor&where=ano%3D2021&order_by=distrito&limit=100"
}
# Diccionario para almacenar los datos obtenidos de las APIs
datos_apis = {}

# Obtener los datos de ambas APIs
for nombre, url in apis.items():
    datos_apis[nombre] = obtener_datos_api(url)

    # Convertir los datos de zonas infantiles a DataFrame
    zonas_infantiles = datos_apis["zonas_infantiles"]
    df_zonas_infantiles = pd.DataFrame([
        {
            "distrito": record["distrito"],
            "valor": record["valor"]
        }
        for record in zonas_infantiles["results"]
    ])

    # Normalizar los nombres de los barrios para compararlos fácilmente
    df_geo["nombre_barrio"] = df_geo["barrio"].apply(normalizar_nombre_barrio)
    df_zonas_infantiles["nombre_barrio"] = df_zonas_infantiles["barrio"].apply(normalizar_nombre_barrio)

    # Realizar el merge entre los DataFrames por el nombre del barrio
    df_merged = pd.merge(
        df_geo[['id', 'nombre_barrio']],
        df_zonas_infantiles,
        on="nombre_barrio",
        how="left"  # Mantener todos los barrios aunque no tengan zonas infantiles
    )

    # Rellenar los valores NaN con 0 (si es necesario)
    df_merged = df_merged.fillna(0)

    # Ajustar la configuración de Pandas para mostrar todas las filas y columnas
    pd.set_option('display.max_rows', None)  # Para mostrar todas las filas
    pd.set_option('display.max_columns', None)  # Para mostrar todas las columnas
    pd.set_option('display.width', None)  # Para ajustar el ancho de la salida
    pd.set_option('display.max_colwidth', None)  # Para mostrar contenido de las celdas sin recortes

    print(df_merged)
else:
    print("Error: Una o ambas APIs no devolvieron datos válidos.")
