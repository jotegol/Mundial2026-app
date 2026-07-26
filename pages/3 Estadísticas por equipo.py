import streamlit as st
import pandas as pd
import numpy as np

#Cargar datos
data = pd.read_csv('data_procesada.csv')

st.set_page_config(
    page_title="Estadísticas Copa Mundial 2026",
    page_icon=":soccer:",
)

# 1. Definición de métricas por lógica de ranking
# Métricas donde MENOS es mejor (Rank 1 es el que tiene el valor más bajo)
metricas_negativas = [
    'goles recibidos x p90', 'gol en propia puerta p90', 'faltas cometidas p90', 
    'tarjetas amarillas p90', 'tarjetas rojas p90', 'dobles amonestaciones p90', 
    'fueras de juego p90', 'tiros fuera p90', 'tiempo recuperacion balon promedio'
]

# Columnas de contexto que no se rankean
metadatos = ['equipo', 'minutos', 'partidos', 'fase']

# 2. Función para calcular los rankings de tu dataset 'data'
def calcular_rankings(df):
    df_ranked = df.copy()
    
    # Identificamos todas las columnas estadísticas (excluyendo metadatos)
    todas_las_stats = [col for col in df.columns if col not in metadatos]
    metricas_positivas = [col for col in todas_las_stats if col not in metricas_negativas]
    
    # Calculamos rankings (Positivas: más alto es el #1 | Negativas: más bajo es el #1)
    for col in metricas_positivas:
        df_ranked[f"{col}_rank"] = df_ranked[col].rank(ascending=False, method='min').astype(int)
        
    for col in metricas_negativas:
        if col in df_ranked.columns: # Por seguridad, verificamos que exista
            df_ranked[f"{col}_rank"] = df_ranked[col].rank(ascending=True, method='min').astype(int)
            
    return df_ranked

# --- AQUÍ CARGAS TU DATASET --- 
df = calcular_rankings(data)

# 3. Encabezado e Interfaz principal
st.title(":1st_place_medal: Estadísticas por equipo")
st.markdown("Analiza el rendimiento p90 y la clasificación en cada métrica respecto a las 48 selecciones.")
st.divider()

# Selector de equipo
# 1. Extraemos la lista de equipos ordenada
lista_equipos = df['equipo'].sort_values().unique().tolist()
# 2. Inicializamos la variable en memoria si es la primera vez que se entra a la página.
# Le asignamos el primer equipo de la lista como valor por defecto.
if 'equipo_seguro' not in st.session_state:
    st.session_state['equipo_seguro'] = lista_equipos[0]
# 3. Buscamos en qué posición (índice) de la lista está el equipo guardado en memoria
indice_guardado = lista_equipos.index(st.session_state['equipo_seguro'])
# 4. Mostramos el selectbox forzando que empiece en la posición que encontramos
team_selected = st.selectbox(
    "Selecciona un equipo:", 
    lista_equipos,
    index=indice_guardado
)
# 5. Actualizamos la memoria instantáneamente con el valor visible en el selectbox
st.session_state['equipo_seguro'] = team_selected

# Obtener datos del equipo
team_data = df[df['equipo'] == team_selected].iloc[0]

# Mostramos el contexto (Minutos, Partidos, Fase)
st.subheader(f"Perfil: {team_selected}")
st.caption(f"Fase alcanzada: {team_data.get('fase', 'N/A')} | Partidos: {team_data.get('partidos', 'N/A')} | Minutos jugados: {team_data.get('minutos', 'N/A')}")

# 4. Agrupación táctica para la interfaz (Categorización)
grupos_estadisticos = {
    "Ataque y Remates": [
        'goles p90', 'goles esperados p90', 'remate p90', 'remate entre los tres palos p90',
        'tiros dentro del área p90', 'tiros fuera del área p90', 'remates de cabeza p90',
        'asistencias p90', 'tiros fuera p90', 'fueras de juego p90'
    ],
    "Distribución y Creación": [
        'posesión del balón promedio', 'precisión en los pases (%)', 'pase p90', 
        'pases completados p90', 'precisión en los centros (%)', 'centros p90',
        'acierto en los cambios de orientación (%)', 'cambios de orientación intentados p90',
        'acierto en las rupturas de líneas (%)', 'intentos de ruptura de líneas p90',
        'regates completados p90', 'saque de esquina p90'
    ],
    "Movimiento y Desmarques": [
        'desmarques para recibir p90', 'desmarques a la espalda de la defensa p90',
        'desmarques entre líneas p90', 'desmarques por delante de la defensa p90',
        'desmarques en el interior de las líneas rivales p90', 'desmarques en el exterior de las líneas rivales p90',
        'recepciones a la espalda de la defensa p90', 'recepciones entre la línea de medias y la defensiva p90',
        'recepciones bajo presión p90'
    ],
    "Defensa y Físico": [
        'pérdidas de balón provocadas p90', 'presiones defensivas p90', 'presiones defensivas directas p90',
        'velocidad media (kmh)', 'distancia recorrida p90', 'esprint a gran velocidad p90', 
        'esprints p90', 'tiempo recuperacion balon promedio', 'faltas cometidas p90', 
        'faltas recibidas p90', 'tarjetas amarillas p90', 'tarjetas rojas p90', 'dobles amonestaciones p90'
    ],
    "Portería": [
        'goles recibidos x p90', 'porterías a cero p90', 'paradas de la portera p90',
        'acciones del portero dentro del área p90', 'acciones del portero fuera del área p90',
        'gol en propia puerta p90'
    ]
}

# 5. Renderizado en Pestañas (Tabs)
tabs = st.tabs(list(grupos_estadisticos.keys()))

# Asumiendo un total de 48 equipos
TOTAL_EQUIPOS = 48

for tab, (nombre_grupo, metricas) in zip(tabs, grupos_estadisticos.items()):
    with tab:
        columnas = st.columns(4)
        col_idx = 0
        
        for stat in metricas:
            if stat in df.columns:
                valor = round(team_data[stat], 2) if isinstance(team_data[stat], (int, float)) else team_data[stat]
                ranking = team_data[f"{stat}_rank"]
                
                # --- LÓGICA DE COLORES ---
                if ranking <= 5:
                    color = "normal"  # Al ser texto sin '-', 'normal' lo pinta Verde
                elif ranking >= (TOTAL_EQUIPOS - 4): # Del 44 al 48 inclusive
                    color = "inverse" # Al ser texto sin '-', 'inverse' lo pinta Rojo
                else:
                    color = "off"     # Gris neutral para el resto
                
                with columnas[col_idx % 4]:
                    st.metric(
                        label=stat.replace(" p90", "").title(),
                        value=valor,
                        delta=f"Rank: {ranking} / 48",
                        delta_color=color # Aplicamos la variable de color dinámica
                    )
                col_idx += 1