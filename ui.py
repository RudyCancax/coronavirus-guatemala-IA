# Importamos streamlit 
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

import sys, os
sys.path.append(os.path.abspath('./'))

# Importamos las funciones de KPI
from kpi import total_casos_guatemala, ploteo_guatemala, ploteo_predicciones

""" 
    Explicación funciones importadas de KPI
     1- total_casos_guatemala
     2- ploteo_guatemala
     3- plotep_predicciones

    (1)
    Se le envía un entero, ej: total_casos_guatemala(0)
    esto para seleccionar que tipo de datos quiero
     - 0: Positivos
     - 1: Recuperados
     - 2: Fallecidos

    y devuelve 1 arreglo de 2 posiciones
    [0]: Un entero con el total de casos solicitado
    [1]: La Fecha del último registro según el archivo csv

    (2)
    Al igual que la función 'total_casos_guatemala',se le envía un entero, ej: ploteo_guatemala(0)
    y Grafica según se el parámetro seleccionado

    (3)
    Al igual que la función 'total_casos_guatemala',se le envía un entero, ej: ploteo_guatemala(0)
    y Grafica según se el parámetro seleccionado
"""


st.sidebar.image('src/mapa_ubicacion.png', format='PNG', width=150)
st.sidebar.title('GRAFICA POR PAIS')

# Diseño de Interfaz de la Aplicación Web
def encabezado_y_graficas_guatemala():
    st.title("CORONAVIRUS EN **GUATEMALA**")
    st.subheader("Fecha de última actualización: " + str(total_casos_guatemala(0)[1]))
    st.image('src/bandera.jpg', use_column_width=True)

    # Datos Positivos
    st.title(str(total_casos_guatemala(0)[0]) + ' - Casos Positivos en Guatemala')
    # Gráfica Casos POSITIVOS Guatemala con prediccion
    ploteo_guatemala(0)

    # Datos Recuperados
    st.title(str(total_casos_guatemala(1)[0]) + '  - Casos Recuperados en Guatemala')
    # Gráfica Casos RECUPERADOS Guatemala con prediccion
    ploteo_guatemala(1)

    # Datos Fallecidos
    st.title(str(total_casos_guatemala(2)[0]) + '  - Casos Fallecidos en Guatemala')
    # Gráfica Casos RECUPERADOS Guatemala con prediccion
    ploteo_guatemala(2)



# Función que ejecuta la función del kpi ploteo_predic para cada pais que sea seleccionado
def grafica_otros_paises():
    st.image('src/mundo.png', format='PNG', width=130)
    ploteo_predicciones(0)
    ploteo_predicciones(1)