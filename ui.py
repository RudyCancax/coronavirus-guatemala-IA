# Importamos streamlit 
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

import sys, os
sys.path.append(os.path.abspath('./'))

from kpi import total_positivos_guatemala, total_fallecidos_guatemala, total_recuperados_guatemala, ploteo_casos_guatemala
# Datos Guatemala
casos_positivos_guate = total_positivos_guatemala()
casos_fallecidos_guate = total_fallecidos_guatemala()
casos_recuperados_guate = total_recuperados_guatemala()
plot = ploteo_casos_guatemala()
# datos_otros_paises = total_positivos_otros_paises()



# Diseño de Interfaz de la Aplicación Web
def encabezado():
    st.title("CORONAVIRUS EN **GUATEMALA**")
    st.subheader("Fecha de última actualización: " + str(casos_positivos_guate[1]))
    # Datos Positivos
    st.header("*CASOS POSITIVOS: *" + str(casos_positivos_guate[0]) 
    + ' - '+ "*CASOS FALLECIDOS: *" + str(casos_fallecidos_guate[0]) 
    + ' - '+ "*CASOS RECUPERADOS: *" + str(casos_recuperados_guate[0]))
    # Datos Fallecidos
    # st.subheader("CASOS DE OTROS PAISES: ", datos_otros_paises)


def ploteo():
    chart_data = pd.DataFrame(
        (plot[2], plot[1]),
        columns=['What']
    )
    st.line_chart(chart_data)