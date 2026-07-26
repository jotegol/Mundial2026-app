import streamlit as st
import pandas as pd
import numpy as np

# Cargar datos
data = pd.read_csv('data_procesada.csv')

st.set_page_config(
    page_title="Estadísticas Copa Mundial 2026",
    page_icon=":soccer:",
)

# 1. Definición de métricas por lógica de ranking
metricas_negativas = [
    'goles recibidos x p90', 'gol en propia puerta p90', 'faltas cometidas p90', 
    'tarjetas amarillas p90', 'tarjetas rojas p90', 'dobles amonestaciones p90', 
    'fueras de juego p90', 'tiros fuera p90', 'tiempo recuperacion balon promedio'
]

# Columnas de contexto que no se rankean
metadatos = ['equipo', 'minutos', 'partidos', 'fase']

# 2. Función para calcular los rankings
def calcular_rankings(df):
    df_ranked = df.copy()
    todas_las_stats = [col for col in df.columns if col not in metadatos]
    metricas_positivas = [col for col in todas_las_stats if col not in metricas_negativas]
    
    for col in metricas_positivas:
        df_ranked[f"{col}_rank"] = df_ranked[col].rank(ascending=False, method='min').astype(int)
        
    for col in metricas_negativas:
        if col in df_ranked.columns:
            df_ranked[f"{col}_rank"] = df_ranked[col].rank(ascending=True, method='min').astype(int)
            
    return df_ranked

df = calcular_rankings(data)
TOTAL_EQUIPOS = len(df['equipo'].unique()) # Se ajusta automáticamente a 48

# 3. Encabezado e Interfaz principal
st.title("⚔️ Comparativa Head-to-Head")
st.markdown("Compara el rendimiento y el ranking de dos selecciones lado a lado.")
st.divider()

# --- SELECTORES DE EQUIPO (EN 2 COLUMNAS) ---
col_sel_1, col_sel_2 = st.columns(2)
lista_equipos = df['equipo'].sort_values().unique().tolist()

# Equipo 1
with col_sel_1:
    if 'equipo_1' not in st.session_state:
        st.session_state['equipo_1'] = lista_equipos[0]
    idx_1 = lista_equipos.index(st.session_state['equipo_1'])
    team_1 = st.selectbox("Selecciona el Equipo A:", lista_equipos, index=idx_1, key="sel_eq_1")
    st.session_state['equipo_1'] = team_1

# Equipo 2
with col_sel_2:
    if 'equipo_2' not in st.session_state:
        # Por defecto seleccionamos el segundo equipo de la lista para que no sean el mismo
        st.session_state['equipo_2'] = lista_equipos[1] if len(lista_equipos) > 1 else lista_equipos[0]
    idx_2 = lista_equipos.index(st.session_state['equipo_2'])
    team_2 = st.selectbox("Selecciona el Equipo B:", lista_equipos, index=idx_2, key="sel_eq_2")
    st.session_state['equipo_2'] = team_2

# Obtener datos de ambos equipos
data_eq_1 = df[df['equipo'] == team_1].iloc[0]
data_eq_2 = df[df['equipo'] == team_2].iloc[0]

# --- PERFILES Y CONTEXTO ---
col_perfil_1, col_perfil_2 = st.columns(2)
with col_perfil_1:
    st.subheader(f"🛡️ {team_1}")
    st.caption(f"Fase: {data_eq_1.get('fase', 'N/A')} | Partidos: {data_eq_1.get('partidos', 'N/A')} | Minutos: {data_eq_1.get('minutos', 'N/A')}")
with col_perfil_2:
    st.subheader(f"🛡️ {team_2}")
    st.caption(f"Fase: {data_eq_2.get('fase', 'N/A')} | Partidos: {data_eq_2.get('partidos', 'N/A')} | Minutos: {data_eq_2.get('minutos', 'N/A')}")
st.divider()

# 4. Agrupación táctica
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

# --- FUNCIÓN REUTILIZABLE PARA RENDERIZAR MÉTRICAS ---
def renderizar_metricas(team_data, metricas):
    # Usamos 2 columnas internas por equipo (lo que da 4 columnas totales en la pantalla)
    cols = st.columns(2)
    col_idx = 0
    
    for stat in metricas:
        if stat in df.columns:
            valor = round(team_data[stat], 2) if isinstance(team_data[stat], (int, float)) else team_data[stat]
            ranking = team_data[f"{stat}_rank"]
            
            # Lógica de colores (Ajustado dinámicamente al total de equipos)
            if ranking <= 5:
                color = "normal" 
            elif ranking >= (TOTAL_EQUIPOS - 4): 
                color = "inverse"
            else:
                color = "off"
            
            with cols[col_idx % 2]:
                st.metric(
                    label=stat.replace(" p90", "").title(),
                    value=valor,
                    delta=f"Rank: {ranking} / {TOTAL_EQUIPOS}",
                    delta_color=color
                )
            col_idx += 1

# 5. Renderizado en Pestañas (Tabs)
tabs = st.tabs(grupos_estadisticos.keys())

for tab, (nombre_grupo, metricas) in zip(tabs, grupos_estadisticos.items()):
    with tab:
        # Dividimos la pestaña a la mitad (Equipo 1 | Equipo 2)
        col_izq, col_der = st.columns(2)
        
        with col_izq:
            # Envolvemos las métricas en una "tarjeta" con borde
            with st.container(border=True):
                # Opcional: un pequeño subtítulo para recordar qué equipo es cada lado
                #st.markdown(f"<p style='text-align: center; color: gray; font-weight: bold;'>{team_1}</p>", unsafe_allow_html=True)
                renderizar_metricas(data_eq_1, metricas)
            
        with col_der:
            # Envolvemos las métricas en una "tarjeta" con borde
            with st.container(border=True):
                #st.markdown(f"<p style='text-align: center; color: gray; font-weight: bold;'>{team_2}</p>", unsafe_allow_html=True)
                renderizar_metricas(data_eq_2, metricas)