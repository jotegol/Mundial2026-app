import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st

#Cargar datos
data = pd.read_csv('data_procesada.csv')

st.set_page_config(
    page_title="Estadísticas Copa Mundial 2026",
    page_icon=":soccer:",
)

st.title("📊 Análisis univariado")

#Selección de variable a graficar
st.write('Analiza el rendimiento de los equipos en cada una de las métricas disponibles. Métricas por 90 minutos (p90) o porcentaje promedio por partido.')
st.divider()
variables = ['velocidad media (kmh)', 'posesión del balón promedio',
       'acierto en los cambios de orientación (%)',
       'precisión en los pases (%)', 'precisión en los centros (%)',
       'acierto en las rupturas de líneas (%)', 'minutos', 'partidos',
       'pérdidas de balón provocadas p90', 'presiones defensivas p90',
       'presiones defensivas directas p90', 'goles recibidos x p90',
       'gol en propia puerta p90', 'faltas recibidas p90',
       'faltas cometidas p90', 'tarjetas amarillas p90', 'fueras de juego p90',
       'tarjetas rojas p90', 'dobles amonestaciones p90',
       'acciones del portero dentro del área p90',
       'acciones del portero fuera del área p90', 'paradas de la portera p90',
       'porterías a cero p90', 'desmarques para recibir p90',
       'desmarques a la espalda de la defensa p90',
       'desmarques entre líneas p90',
       'desmarques por delante de la defensa p90',
       'desmarques en el interior de las líneas rivales p90',
       'desmarques en el exterior de las líneas rivales p90',
       'recepciones a la espalda de la defensa p90',
       'recepciones entre la línea de medias y la defensiva p90',
       'recepciones bajo presión p90', 'esprint a gran velocidad p90',
       'esprints p90', 'distancia recorrida p90', 'remate p90',
       'goles esperados p90', 'goles p90', 'asistencias p90',
       'remate entre los tres palos p90', 'tiros fuera p90',
       'tiros dentro del área p90', 'tiros fuera del área p90',
       'remates de cabeza p90', 'saque de esquina p90', 'pase p90',
       'pases completados p90', 'centros p90',
       'intentos de ruptura de líneas p90', 'regates completados p90',
       'cambios de orientación intentados p90',
       'tiempo recuperacion balon promedio']

# Selector de variable
if 'variable_segura' not in st.session_state:
    st.session_state['variable_segura'] = variables[0]
# 3. Buscamos en qué posición (índice) de la lista está el equipo guardado en memoria
indice_guardado = variables.index(st.session_state['variable_segura'])
# 4. Mostramos el selectbox forzando que empiece en la posición que encontramos
variable = st.selectbox(
    "Elige una variable a graficar:", 
    variables,
    index=indice_guardado
)
# 5. Actualizamos la memoria instantáneamente con el valor visible en el selectbox
st.session_state['variable_segura'] = variable


col1, col2 = st.columns(2)
with col1:
    equipos = st.radio("Elige equipos a mostrar:", ("5 Más altos", "5 más bajos", "Todos los equipos"))
with col2:
    orden = st.radio("Elige el orden de la gráfica:", ("Ascendente", "Descendente"))


if equipos == "5 Más altos":
    data = data.sort_values(by=variable, ascending=False).head(5)
    altura = None
elif equipos == "5 más bajos":
    data = data.sort_values(by=variable, ascending=True).head(5)
    altura = None
else:
    data = data.sort_values(by=variable, ascending=True)
    altura = 1200
#Gráfico
figura = px.bar(
    data,
    x=variable,
    y='equipo',
    orientation='h',
    color='fase', # Colorea por fase
    color_discrete_map={'Ganador': 'gold', 'Semifinalista': 'blue', 'Primera fase': 'lightgray', 'Segunda fase': 'lightblue'},
    title=f"Comparación de {variable} entre equipos",
    labels={variable: variable, 'equipo': 'Equipo'},
    # Le damos más altura para que 48 barras respiren bien (ej. 1000px o 1200px)
    height=altura  
)
figura.update_yaxes(
    type='category', 
    dtick=1,
    categoryorder='total ascending' if orden == "Ascendente" else 'total descending' # <--- Fuerza el orden por el valor numérico
)
figura.update_layout(
    # 1. Movemos la leyenda debajo del gráfico para liberar ancho
    legend=dict(
        orientation="h",       # Leyenda horizontal
        yanchor="top",
        y=-0.15,               # Posición debajo del eje X
        xanchor="center",
        x=0.5                  # Centrada
    )
)
st.plotly_chart(figura, use_container_width=True)