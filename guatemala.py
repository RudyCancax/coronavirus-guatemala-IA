import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from kpi import total_casos_guatemala

def poblacion_guate():
    poblacion = pd.read_csv('https://raw.githubusercontent.com/RudyCancax/documentos/master/poblacion_guatemala_2018.csv')
    return poblacion


def grafica():
    poblacion = int(total_poblacion_guatemala())
    positivos = int(total_casos_guatemala(0)[0])
    recuperados = int(total_casos_guatemala(1)[0])
    fallecidos = int(total_casos_guatemala(2)[0])


    labels = ['Población Total','Positivos', 'Recuperados', 'Fallecidos']
    valores = [poblacion, positivos, recuperados, fallecidos]

    # pull is given as a fraction of the pie radius
    fig = go.Figure(data=[go.Bar(x=labels, y=valores, text=valores, textposition='auto')])
    st.plotly_chart(fig)


def total_poblacion_guatemala():
    data = poblacion_guate()
    total = int(data['Población total'].sum())
    return total
