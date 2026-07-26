import streamlit as st


st.write("# Estadísticas Copa Mundial de la FIFA 2026 :trophy::soccer:")

st.subheader("Autor: Rodrigo Olagnier Pérez")

st.sidebar.success("Selecciona estadísticas a consultar.")

st.markdown(
    """
    Bienvenido/a! la siguiente aplicación permite explorar de forma interactiva 
    las estadísticas de los 48 participantes de la Copa Mundial de la FIFA 2026. Las estadísticas disponibles son porcentajes promedio por partido o frecuencia cada 90 minutos (p90).\n
    **👈 Escoge en la barra lateral lo que quieras consultar. ¿Cuales son las opciones disponibles?**
    - Análisis univariado: Permite revisar la clasificación de los equipos en una métrica específica
    - Análisis bivariado: Permite analizar la relación entre dos métricas específicas
    - Estadísticas por equipo: Permite revisar el desempeño de un equipo en todas las métricas disponibles
    - Comparativa: Permite comparar el desempeño de dos equipos en todas las métricas disponibles
    ### Fuente de los datos
    - Los datos fueron obtenidos del [registro oficial de estadísticas de la FIFA](https://www.fifa.com/es/tournaments/mens/worldcup/canadamexicousa2026/statistics/team-statistics)

    ### Otras fuentes de datos relacionadas
    - [FBREF](https://fbref.com/en/comps/1/stats/World-Cup-Stats)
    - [WhoScored](https://es.whoscored.com/regions/247/tournaments/36/seasons/10498/stages/23752/teamstatistics/internacional-fifa-world-cup-2026)
    - [Sofascore](https://www.sofascore.com/es-la/football/tournament/world/world-championship/16#id:58210)
"""
)

