import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

# Fonction pour tester la stationnarité d'une série
def test_stationarity(series):
    result = adfuller(series.dropna())
    return result[1] < 0.05  # Retourne True si la série est stationnaire

# Fonction pour rendre une série stationnaire
def make_series_stationary(series, max_diff=5):
    diff_count = 0
    while not test_stationarity(series) and diff_count < max_diff:
        series = series.diff()
        diff_count += 1
    return series, diff_count
