import streamlit as st

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from datetime import datetime, timedelta
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

import plotly.graph_objects as go
import plotly_express as px



# Definición de funciones a utilizar para las predicciones
def logistic(t, a, b, c, d):
    return c + (d - c)/(1 + a * np.exp(- b * t))

def exponential(t, a, b, c):
    return a * np.exp(b * t) + c

def linear_prediction(x_train, y_train, x_pred_len, x_range):
    x_samp, y_samp = np.reshape(x_train, (-1, 1)), np.reshape(y_train, (-1, 1))        # 1
    model = LinearRegression().fit(x_samp, y_samp)
    test_x = np.arange(x_pred_len)
    y_fit = model.predict(test_x.reshape (-1, 1))
    linear_plot = go.Scatter(
        x=x_range,
        y=np.round_(y_fit.reshape(y_fit.size)),
        mode='lines',
        name='Linear'
    )
    return y_fit, linear_plot

def logistic_prediction(x_train, y_train, x_pred_len, x_range):
    test_x = np.arange(x_pred_len)
    lpopt, lpcov = curve_fit(logistic, x_train, y_train, maxfev=10000)
    lerror = np.sqrt(np.diag(lpcov))

    # for logistic curve at half maximum, slope = growth rate/2. so doubling time = ln(2) / (growth rate/2)
    ldoubletime = np.log(2)/(lpopt[1]/2)
    # standard error
    ldoubletimeerror = 1.96 * ldoubletime * np.abs(lerror[1]/lpopt[1])

    # calculate R^2
    residuals = y_train - logistic(x_train, *lpopt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_train - np.mean(y_train))**2)
    logisticr2 = 1 - (ss_res / ss_tot)  
    
    y_fit = logistic(test_x, *lpopt)

    if logisticr2 > 0.95:
        logistic_plot = go.Scatter(
            x=x_range,
            y=np.round_(y_fit),
            mode='lines',
            name='Logistica'
        )
        print('\n** Con ajuste lineal**\n')
        print('\tR^2:', logisticr2)
        print('\tTiempo para duplicarse (ritmo actual): ', round(ldoubletime,2), '(±', round(ldoubletimeerror,2),') días')
        logisticworked = True

        return y_fit, logistic_plot  
    return y_fit, None


def exponential_prediction(x_train, y_train, x_pred_len, x_range):
    epopt, epcov = curve_fit(exponential, x_train, y_train, bounds=([0,0,-100],[100,0.9,100]), maxfev=10000)
    eerror = np.sqrt(np.diag(epcov))

    # for exponential curve, slope = growth rate. so doubling time = ln(2) / growth rate
    edoubletime = np.log(2)/epopt[1]
    # standard error
    edoubletimeerror = 1.96 * edoubletime * np.abs(eerror[1]/epopt[1])

    # calculate R^2
    residuals = y_train - exponential(x_train, *epopt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_train - np.mean(y_train))**2)
    expr2 = 1 - (ss_res / ss_tot)
    
    test_x = np.arange(x_pred_len)
    y_fit = exponential(test_x, *epopt)

    if expr2 > 0.95:
        exponential_plot = go.Scatter(
            x=x_range,
            y=np.round_(y_fit),
            mode='lines',
            name='Exponencial'
        )
        print('\n** Con ajuste exponencial **\n')
        print('\tR^2:', expr2)
        print('\tTiempo para duplicarse (ritmo actual): ', round(edoubletime,2), '(±', round(edoubletimeerror,2),') días')
        exponentialworked = True
        return y_fit, exponential_plot
    return y_fit, None