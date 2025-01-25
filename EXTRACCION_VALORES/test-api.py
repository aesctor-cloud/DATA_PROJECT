import requests
import pandas as pd
import streamlit as st
# import geopandas as gpd
# from shapely.geometry import Polygon
import plotly.express as px

apis = {
    "geo" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/barris-barrios/records?limit=100",
    "alquiler" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/precio-alquiler-vivienda/records?select=codbar_coddistrit%2C%20avg(precio_2022_euros_m2)%20as%20precio_alquiler_m2&group_by=codbar_coddistrit&limit=100",
    "compra" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/precio-de-compra-en-idealista/records?select=coddistbar%2C%20avg(precio_2022_euros_m2)%20as%20precio_compra_m2&group_by=coddistbar&limit=100",
    "metro" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/transporte-barrios/records?select=coddistbar%2C%20count(distinct%20stop_id)%20as%20paradas_metro&where=transporte%3D%27metrovlc%27&group_by=coddistbar&limit=100",
    "bus" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/transporte-barrios/records?select=coddistbar%2C%20count(distinct%20stop_id)%20as%20paradas_bus&where=transporte%3D%27emt%27&group_by=coddistbar&limit=100",
    "vulnerabilidad" :"https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/vulnerabilidad-por-barrios/records?select=codbar%2C%20avg(ind_global)%20as%20vulnerabilildad&group_by=codbar&limit=100",
    "hospitales" : "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/hospitales/records?select=coddistbar%2C%20count(distinct%20nombre)%20as%20hospitales&where=tipo%3D%22Hospital%22&group_by=coddistbar&limit=100"
}

def obtener_datos_api(api_url):
    response = requests.get(api_url)
    return response.json()

datos_apis = {}

for nombre, url in apis.items():
    datos_apis[nombre] = obtener_datos_api(url)

# Geo
geo = datos_apis["geo"]

df_geo = pd.DataFrame([
        {
            "id": record["coddistbar"],
            "barrio": record["nombre"],
            "geometry": record["geo_shape"]["geometry"],
            "lat": record["geo_point_2d"]["lat"],
            "lon": record["geo_point_2d"]["lon"]
        }
        for record in geo["results"]
    ])

# Alquiler
alquiler = datos_apis["alquiler"]

df_alquiler = pd.DataFrame([
        {
            "id": record["codbar_coddistrit"],
            "precio_alquiler": record["precio_alquiler_m2"]
        }
        for record in alquiler["results"]
    ])

min_alquiler = df_alquiler['precio_alquiler'].min()
max_alquiler = df_alquiler['precio_alquiler'].max()

df_alquiler['precio_alquiler_normalizado'] = 1 - (df_alquiler['precio_alquiler'] - min_alquiler) / (max_alquiler - min_alquiler)

# Compra
compra = datos_apis["compra"]

df_compra = pd.DataFrame([
        {
            "id": record["coddistbar"],
            "precio_compra": record["precio_compra_m2"]
        }
        for record in compra["results"]
    ])

min_compra = df_compra['precio_compra'].min()
max_compra = df_compra['precio_compra'].max()

df_compra['precio_compra_normalizado'] = 1 - (df_compra['precio_compra'] - min_compra) / (max_compra - min_compra)

# Metro
metro = datos_apis["metro"]

df_metro = pd.DataFrame([
        {
            "id": record["coddistbar"],
            "paradas_metro": record["paradas_metro"]
        }
        for record in metro["results"]
    ])

min_metro = df_metro['paradas_metro'].min()
max_metro = df_metro['paradas_metro'].max()

df_metro['paradas_metro_normalizado'] = (df_metro['paradas_metro'] - min_metro) / (max_metro - min_metro)

# Bus
bus = datos_apis["bus"]

df_bus = pd.DataFrame([
        {
            "id": record["coddistbar"],
            "paradas_bus": record["paradas_bus"]
        }
        for record in bus["results"]
    ])

min_bus = df_bus['paradas_bus'].min()
max_bus = df_bus['paradas_bus'].max()

df_bus['paradas_bus_normalizado'] = (df_bus['paradas_bus'] - min_bus) / (max_bus - min_bus)

# Vulnerabilidad
vulne = datos_apis["vulnerabilidad"]

df_vulne = pd.DataFrame([
        {
            "id": record["codbar"],
            "vulne": record["vulnerabilildad"]
        }
        for record in vulne["results"]
    ])

min_vulne = df_vulne['vulne'].min()
max_vulne = df_vulne['vulne'].max()

df_vulne['vulne_normalizado'] = 1 - (df_vulne['vulne'] - min_vulne) / (max_vulne - min_vulne)

# Hospitales
hospi = datos_apis["hospitales"]

df_hospi = pd.DataFrame([
        {
            "id": record["coddistbar"],
            "hospitales": record["hospitales"]
        }
        for record in hospi["results"]
    ])

min_hospi = df_hospi['hospitales'].min()
max_hospi = df_hospi['hospitales'].max()

df_hospi['hospitales_normalizado'] = (df_hospi['hospitales'] - min_hospi) / (max_hospi - min_hospi)


# Merges
df_geo['id'] = df_geo['id'].astype(str)
df_alquiler['id'] = df_alquiler['id'].astype(str)
df_compra['id'] = df_compra['id'].astype(str)
df_metro['id'] = df_metro['id'].astype(str)
df_bus['id'] = df_bus['id'].astype(str)
df_vulne['id'] = df_vulne['id'].astype(str)
df_hospi['id'] = df_hospi['id'].astype(str)

df_base = pd.merge(df_geo, df_alquiler, on='id', how='left')
df_base = pd.merge(df_base, df_compra, on='id', how='left')
df_base = pd.merge(df_base, df_metro, on='id', how='left')
df_base = pd.merge(df_base, df_bus, on='id', how='left')
df_base = pd.merge(df_base, df_vulne, on='id', how='left')
df_base = pd.merge(df_base, df_hospi, on='id', how='left')

df_base = df_base.fillna(0)

df_base = df_base[['id', 'barrio', 'geometry', 'lat', 'lon', 'precio_alquiler_normalizado', 'precio_compra_normalizado', 'paradas_metro_normalizado', 'paradas_bus_normalizado', 'vulne_normalizado', 'hospitales_normalizado']]

df_base = df_base.rename(columns={
    'lat': 'lat',
    'lon': 'lon',
    'precio_alquiler_normalizado': 'el precio del alquiler',
    'precio_compra_normalizado': 'el precio de compra',
    'paradas_metro_normalizado': 'las paradas de metro',
    'paradas_bus_normalizado': 'las paradas de autobús',
    'vulne_normalizado': 'la tasa de vulnerabilidad',
    'hospitales_normalizado': 'los hospitales cercanos'
})


# metemos la app

# Hacemos una copia del dataframe para que pondere luego
df_ponderado = df_base.copy()

# Título
st.title("Encuentra el mejor barrio para tu nueva vivienda")
st.write("#### La única aplicación que se adapta a lo que verdaderamente te importa:")

# st.dataframe(df_base)

st.write("Para personalizar tu búsqueda, contesta las siguientes preguntas (siendo 0 'Nada importante' y 5 'Muy importante'")

# Lista de los factores
factores = ['el precio del alquiler', 'el precio de compra', 'las paradas de metro', 'las paradas de autobús','la tasa de vulnerabilidad','los hospitales cercanos']

# Diccionario para respuestas formulario
respuestas = {}

# Formulario y recogida en diccionario
with st.form(key="form"):
    for factor in factores:
        respuestas[factor] = st.slider( # poniendo [factor] estamos indicando que es la key del diccionario
            f"¿Cómo de importante es para ti {factor}?", 
            0,5,0
            ) # la opción elegida es el valor del diccionario
    enviar = st.form_submit_button("Enviar preferencias")

if enviar:

    # Generamos las ponderaciones para que multiplique
    ponderaciones = { 
        0: 0,
        1: 0.5, 
        2: 0.75, 
        3: 1, 
        4: 1.25, 
        5: 1.50
        }

    # Creamos un nuevo diccionario
    # Este diccionario es como respuestas pero con los valores por los que queremos multiplicar luego
    respuestas_ponderadas = {
        factor: ponderaciones[valoracion] # accedemos al valor en ponderaciones cuya key equivale a lo que se ha respondido
        for factor, valoracion in respuestas.items() # .items devuelve los pares del diccionario
        }
    
    # iloc [filas, columnas] -> cogemos solo las columnas numericas
    df_ponderado.iloc[:, 5:11] *= [respuestas_ponderadas[factor] # busca el número por el que hay que multiplicar para cada factor
                                for factor in factores] # itera sobre la lista inicial de factores sobre la que se basa el formulario

    # añadimos una columna de sumatorio de todos los factores
    df_ponderado['sumatorio'] = (df_ponderado.iloc[:, 5:11].sum(axis=1))

    # ordenamos de manera descendente
    df_ponderado = df_ponderado.sort_values(by='sumatorio', ascending=False)

    # lista top 3 barrios
    # top_barrios = df_ponderado.iloc[:3, 1].tolist()

    st.write(f"")
    st.write(f"")

    top10 = df_ponderado.iloc[:10, [1, 11]]
    top10 = top10.sort_values(by='sumatorio', ascending=True)

    # barras
    barras = px.bar(top10, 
                    x="sumatorio", 
                    y="barrio", 
                    orientation='h',
                    title='Éstos son los mejores barrios según tus preferencias:')
    
    st.plotly_chart(barras)

    # Creamos geojson para que luego lo pueda utilizar plotly
    
    geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "id": row["id"]
            },
            "geometry": row["geometry"]
        }
        for _, row in df_ponderado.iterrows() # va fila a fila del df ignorando índices
    ]
}

    # https://plotly.github.io/plotly.py-docs/generated/plotly.express.choropleth_mapbox.html#:~:text=a%20Mapbox%20map.-,Parameters,-data_frame%20(DataFrame
    mapa = px.choropleth_mapbox(
        df_ponderado, # dataframe
        geojson=geojson, # geojson
        locations="id", # key para cruzar df con geojson
        featureidkey="properties.id",  # key para cruzar geojson con df
        color="sumatorio",  # Métrica para los colores
        color_continuous_scale=[(0, "azure"), (1, "seagreen")],
        hover_name="barrio",
        hover_data=["sumatorio"],
        mapbox_style="carto-positron",
        center={"lat": 39.47, "lon": -0.37},
        zoom=10,
    )

    st.plotly_chart(mapa)