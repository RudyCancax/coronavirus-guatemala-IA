# Importamos streamlit 
import streamlit as st

# Importamos las funciones de prediccion
from funciones import logistic, exponential, linear_prediction, logistic_prediction, exponential_prediction

# manipulacion de dats
import numpy as np
import pandas as pd
import json
import plotly.graph_objects as go
import plotly_express as px

from scipy.optimize import curve_fit
from datetime import datetime, timedelta
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

# herramientas de ML
from sklearn.pipeline import Pipeline


import importlib
from modeler import countries, models
importlib.reload(countries)
importlib.reload(models)
c = countries.CountryData()

paises = []

def leer_archivos_csv():
    datos_positivos = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    datos_recuperados = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    datos_fallecidos = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    return datos_positivos, datos_recuperados, datos_fallecidos

# Variable que almacena los datos leidos
datos_csv = leer_archivos_csv();

# BARRA LATERAL DE NUESTRA APP
def barra_lateral(l):
    p = paises
        # Variable que selecciona que tipo de dato filtrará
    z = int(l)
    d = datos_csv[z]

    texto = ''
    if z == 0:
        texto = '(CASOS POSITIVOS)'
    elif z == 1:
        texto = '(CASOS RECUPERADOS)'
    else:
        texto = '(CASOS FALLECIDOS)'

    # Barra lateral
    st.sidebar.title("Seleccione el Pais según " + texto)

    # Selecció múltiple en barra lateral y se graficará según el o los paises que se seleccionan
    p = st.sidebar.multiselect('',d['Country/Region'].unique())
    return p



# Lee la información y establece el total de
# casos según SE INDIQUE: n=0 (Positivos), n=1 (Recuperados), n=2 (Fallecidos)
def total_casos_guatemala(n):
    # leer archivo principal
    n = int(n)
    data = datos_csv[n]
    casos = data.iloc[:,[1,-1]].groupby('Country/Region').sum()
    fecha_mas_reciente = casos.columns[0]
    casos = casos.sort_values(by = fecha_mas_reciente, ascending = False)
    casos.reset_index(inplace=True)
    casos = casos[casos['Country/Region'].isin(['Guatemala'])]
    total_casos = casos.iat[0,1]
    casos.set_index('Country/Region')
    return total_casos, fecha_mas_reciente


    # Ploteo o graficado
def plotCases(dataframe, column, country):
    co = dataframe[dataframe[column] == country].iloc[:,4:].T.sum(axis = 1)
    co = pd.DataFrame(co)
    co.columns = ['Cases']
    co = co.loc[co['Cases'] > 0]
    
    # Define base training data
    y = np.array(co['Cases'])
    x = np.arange(y.size)
    # Define test size
    x_test_len = round(x.size * 3)
    test_x = np.arange(x_test_len)
    
    start_date = datetime.strptime(co.index[0], '%m/%d/%y').date()
    end_date = start_date + timedelta(days=x_test_len)
    x_range = pd.Series(np.arange(np.datetime64(str(start_date)), np.datetime64(str(end_date))))
    
    recentdbltime = float('NaN')
    
    # get linear model prediction and plot
    linear_y, linear_plot = linear_prediction(x, y, x_test_len, x_range)
    
    if len(y) >= 7:
        
        current = y[-1]
        lastweek = y[-8]
        
        if current > lastweek:
            print('\n** Basado en los datos de la última semana **\n')
            print('\tCasos confirmados en',co.index[-1],'\t',current)
            print('\tCasos confirmados en',co.index[-8],'\t',lastweek)
            ratio = current/lastweek
            print('\tProporción:',round(ratio,2))
            print('\tIncremento semanal:',round( 100 * (ratio - 1), 1),'%')
            dailypercentchange = round( 100 * (pow(ratio, 1/7) - 1), 1)
            print('\tIncremento diario:', dailypercentchange, '% por día')
            recentdbltime = round( 7 * np.log(2) / np.log(ratio), 1)
            print('\tTiempo que tarda en duplicarse (al ritmo actual):',recentdbltime,'días')

    original_data = go.Scatter(
        x=pd.date_range(start=start_date, end=datetime.strptime(co.index[-1], '%m/%d/%y').date()),
        y=y,
        mode='markers',
        name='Casos confirmados'
    )
    plot_data = []
    plot_data.append(original_data)
    plot_data.append(linear_plot)
    
    logisticworked = False
    exponentialworked = False
    
    test_x = np.arange(round(x.size * 2.1))
    
    
    logistic_y, logistic_plot= logistic_prediction(x, y, x_test_len, x_range)
    if logistic_plot:
        plot_data.append(logistic_plot)
    
    
    exponential_y, exponential_plot = exponential_prediction(x, y, x_test_len, x_range)
    if exponential_plot:
        plot_data.append(exponential_plot)
    

    layout = dict(
        title = f'{country}',
        xaxis_type='date'
    )

    fig = go.Figure(data=plot_data, layout=layout)
    st.plotly_chart(fig)

# FIN FUNCIÓN DE GRAFICACIÓN


    

def ploteo_predicciones(a):
    a = int(a)
    datos = datos_csv[a]

    texto = ''
    if a == 0:
        texto = ' - Casos Positivos'
    elif a == 1:
        texto = ' - Casos Recuperados'
    else:
        texto = ' - Casos Fallecidos'

        # Barra lateral para seleccionar pais, según caso 0: positivos, 1: recuperados, 2: fallecidos
    paises = barra_lateral(a)
    cases = datos.iloc[:,[1,-1]].groupby('Country/Region').sum()
    mostrecentdate = cases.columns[0]

    cases = cases.sort_values(by = mostrecentdate, ascending = False)
    cases = cases[(cases[mostrecentdate] >= 10)]
    cases.reset_index(inplace=True)
    cases = cases[cases['Country/Region'].isin(paises)]
    cases.set_index('Country/Region', inplace=True)

    st.title('Otros paises' + texto)
    topcountries = cases.index
    inferreddoublingtime = []
    recentdoublingtime = []
    errors = []
    countries = []
    print('\n')

    for c in topcountries:
        b = plotCases(datos, 'Country/Region', c)
        if b:
            countries.append(c)
            inferreddoublingtime.append(b[0])
            errors.append(b[1])
            recentdoublingtime.append(b[2])
        print('\n')






def ploteo_guatemala(a):
    a = int(a)
    datos = datos_csv[a]

    cases = datos.iloc[:,[1,-1]].groupby('Country/Region').sum()
    mostrecentdate = cases.columns[0]

    cases = cases.sort_values(by = mostrecentdate, ascending = False)
    cases = cases[(cases[mostrecentdate] >= 10)]
    cases.reset_index(inplace=True)
    cases = cases[cases['Country/Region'].isin(['Guatemala'])]
    cases.set_index('Country/Region', inplace=True)

    topcountries = cases.index
    inferreddoublingtime = []
    recentdoublingtime = []
    errors = []
    countries = []
    print('\n')

    for c in topcountries:
        b = plotCases(datos, 'Country/Region', c)
        if b:
            countries.append(c)
            inferreddoublingtime.append(b[0])
            errors.append(b[1])
            recentdoublingtime.append(b[2])
        print('\n')


