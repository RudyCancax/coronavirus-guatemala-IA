# Importamos streamlit 
import streamlit as st

# grafico
import chart_studio
import chart_studio.plotly as py
import plotly.figure_factory as ff

import sys, os
sys.path.append(os.path.abspath('./'))



# Importamos para la interfaz de usuario
from ui import encabezado

encabezado()