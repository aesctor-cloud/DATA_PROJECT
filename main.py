import streamlit as st
from data import get_data
from data import get_mapa
from data import ponderar

st.set_page_config(
    page_title="Encuentra tu barrio ideal",
    page_icon="🏡",
    layout="wide", 
    initial_sidebar_state="collapsed" 
)

# Traemos los datos
df_base = get_data()

# Para el mapa inicial
df_mapa = df_base.copy()
df_mapa['sumatorio'] = (df_mapa.iloc[:, 5:12].sum(axis=1))

# Título
st.title("Encuentra el mejor barrio para tu nueva vivienda")
st.write("#### La única aplicación que se adapta a lo que verdaderamente te importa")
st.write(" ")
st.write(" ")

col1, col2 = st.columns([1,2])

with col1:
    st.write("Para personalizar tu búsqueda, contesta las siguientes preguntas (siendo 0 'Nada importante' y 5 'Muy importante'")

    # Lista de los factores
    factores = ['el precio del alquiler', 'el precio de compra', 'las paradas de metro', 'las paradas de autobús','la tasa de vulnerabilidad','los hospitales cercanos','los parques infantiles cercanos']

    # Diccionario para respuestas formulario
    respuestas = {}

    # Formulario y recogida en diccionario
    with st.form(key="form", border=False):
        for factor in factores:
            respuestas[factor] = st.slider( # poniendo [factor] estamos indicando que es la key del diccionario
                f"¿Cómo de importante es para ti {factor}?", 
                0,5,0
                ) # la opción elegida es el valor del diccionario
        enviar = st.form_submit_button("Enviar preferencias")

with col2:
    st.write(" ")
    st.write(" ")
    
    # Creamos el mapa
    if enviar:
        st.write("#### Nuestra visión inicial:")
        df_ponderado = ponderar(respuestas, df_base)
        mapa = get_mapa(df_ponderado)
    else:
        st.write("#### Los mejores barrios según tus preferencias:")
        mapa = get_mapa(df_mapa)

    st.plotly_chart(mapa)

st.dataframe(df_base)