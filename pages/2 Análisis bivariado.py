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

st.title(":chart_with_upwards_trend: Análisis bivariado")

#Selección de variables a graficar
st.write('Analiza la relación entre dos de las métricas disponibles. Métricas por 90 minutos (p90) o porcentaje promedio por partido.')
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

# Selector de variable X
if 'variable_segura_x' not in st.session_state:
    st.session_state['variable_segura_x'] = variables[0]
# 3. Buscamos en qué posición (índice) de la lista está el equipo guardado en memoria
indice_guardado = variables.index(st.session_state['variable_segura_x'])
# 4. Mostramos el selectbox forzando que empiece en la posición que encontramos
variable_x = st.selectbox(
    "Elige una opción para el eje X:", 
    variables,
    index=indice_guardado
)
# 5. Actualizamos la memoria instantáneamente con el valor visible en el selectbox
st.session_state['variable_segura_x'] = variable_x

# Selector de variable Y
if 'variable_segura_y' not in st.session_state:
    st.session_state['variable_segura_y'] = variables[0]
# 3. Buscamos en qué posición (índice) de la lista está el equipo guardado en memoria
indice_guardado = variables.index(st.session_state['variable_segura_y'])
# 4. Mostramos el selectbox forzando que empiece en la posición que encontramos
variable_y = st.selectbox(
    "Elige una opción para el eje Y:", 
    variables,
    index=indice_guardado
)
# 5. Actualizamos la memoria instantáneamente con el valor visible en el selectbox
st.session_state['variable_segura_y'] = variable_y

#Gráfico
figura = px.scatter(
    data, 
    x= variable_x, 
    y=variable_y,
    text='equipo', # Muestra el nombre del país en el punto
    color='fase', # Colorea por fase
    color_discrete_map={'Ganador': 'gold', 'Semifinalista': 'blue', 'Primera fase': 'lightgray', 'Segunda fase': 'lightblue'},
    title= f"Relación entre {variable_x} y {variable_y}",
    labels={variable_x: variable_x, variable_y: variable_y}
)
z = np.polyfit(data[variable_x], data[variable_y], 1)
p = np.poly1d(z)
figura.add_scatter(x=data[variable_x], y=p(data[variable_x]), mode='lines', line=dict(color='red', width=2), name='Tendencia')
figura.update_traces(textposition='top center')
figura.update_layout(height=600, template='plotly_white')
figura.update_traces(marker=dict(size=10))
st.plotly_chart(figura)