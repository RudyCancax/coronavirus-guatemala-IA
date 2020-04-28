# Importamos streamlit 
import streamlit as st

# manipulacion de dats
import numpy as np
import pandas as pd
import json

from scipy.optimize import curve_fit
from datetime import datetime, timedelta
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score


import sys, os
sys.path.append(os.path.abspath('../'))


import importlib
from modeler import countries, models
importlib.reload(countries)
importlib.reload(models)
c = countries.CountryData()
data = c.get_country('Guatemala', dates=True)
model = models.LinearModel(x_train=data[0], y_train=data[1])
# herramientas de ML
from sklearn.pipeline import Pipeline

def total_positivos_guatemala():

    # leer archivo principal
    positivos = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

    casos_positivos = positivos.iloc[:,[1,-1]].groupby('Country/Region').sum()
    fecha_mas_reciente = casos_positivos.columns[0]
    casos_positivos = casos_positivos.sort_values(by = fecha_mas_reciente, ascending = False)
    casos_positivos.reset_index(inplace=True)
    casos_positivos = casos_positivos[casos_positivos['Country/Region'].isin(['Guatemala'])]
    total_positivos = casos_positivos.iat[0,1]
    casos_positivos.set_index('Country/Region')
    return total_positivos, fecha_mas_reciente



def total_fallecidos_guatemala():
    
    # leer archivo principal
    fallecidos = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

    casos_fallecidos = fallecidos.iloc[:,[1,-1]].groupby('Country/Region').sum()
    fecha_mas_reciente = casos_fallecidos.columns[0]
    casos_fallecidos = casos_fallecidos.sort_values(by = fecha_mas_reciente, ascending = False)
    casos_fallecidos.reset_index(inplace=True)
    casos_fallecidos = casos_fallecidos[casos_fallecidos['Country/Region'].isin(['Guatemala'])]
    total_fallecidos = casos_fallecidos.iat[0,1]
    casos_fallecidos.set_index('Country/Region')
    return total_fallecidos, fecha_mas_reciente



def total_recuperados_guatemala():
    
    # leer archivo principal
    recuperados = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

    casos_recuperados = recuperados.iloc[:,[1,-1]].groupby('Country/Region').sum()
    fecha_mas_reciente = casos_recuperados.columns[0]
    casos_recuperados = casos_recuperados.sort_values(by = fecha_mas_reciente, ascending = False)
    casos_recuperados.reset_index(inplace=True)
    casos_recuperados = casos_recuperados[casos_recuperados['Country/Region'].isin(['Guatemala'])]
    total_recuperados = casos_recuperados.iat[0,1]
    casos_recuperados.set_index('Country/Region')
    return total_recuperados, fecha_mas_reciente


# def total_positivos_otros_paises():
#         # leer archivo principal
#     dts = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

#     pais = st.sidebar.multiselect('Seleccione un pais: ', dts['Country/Region'])
#     casos_paises = dts.iloc[:,[1,-1]].groupby('Country/Region').sum()
#     fecha_mas_reciente = casos_paises.columns[0]
#     casos_paises = casos_paises.sort_values(by = fecha_mas_reciente, ascending = False)
#     casos_paises.reset_index(inplace=True)
#     casos_paises = casos_paises[casos_paises['Country/Region'].isin(pais)]
#     casos_paises.set_index('Country/Region', inplace=True)
#     print(casos_paises)
#     return casos_paises
