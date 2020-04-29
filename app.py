# Importamos streamlit 
import streamlit as st
import streamlit_theme as stt 

# Importamos para la interfaz de usuario
from ui import encabezado_y_graficas_guatemala, grafica_otros_paises

# Datos GUATEMALA
encabezado_y_graficas_guatemala()


# Todas las demás gráficas
grafica_otros_paises()