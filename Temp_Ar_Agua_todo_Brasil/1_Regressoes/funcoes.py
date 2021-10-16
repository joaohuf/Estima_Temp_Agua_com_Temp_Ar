# fit a straight line to the economic data
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, max_error, mean_absolute_percentage_error

# Funcoes usadas para regressao

def linear(x, a, b):
    return a * x + b

def quadratic(x, a, b, c):
    return a * x + b * x**2 + c

def exponential(x, a, b, c):
    return a*np.exp(b*x) + c

def logarithmic(x, a, b):
    return a*np.log(x) + b

def logistic(x, a, b, c, d):
    return -b/(c + np.exp(-a*x)) + d

def best_regression(x, y):
    regressions = [linear, quadratic, exponential, logarithmic, logistic]

    results = []
    for regression in regressions:
        try:
            popt, _, = curve_fit(regression, x, y)

            if len(popt) == 2:
                a, b = popt
                y_pred = regression(x, a, b)
            elif len(popt) == 3:
                a, b, c = popt
                y_pred = regression(x, a, b, c)
            else:
                a, b, c, d = popt
                y_pred = regression(x, a, b, c, d)

            mae = mean_absolute_error(y, y_pred)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            e_max = max_error(y, y_pred)
            r2 = r2_score(y, y_pred)
            mape = mean_absolute_percentage_error(y, y_pred)
            n = len(y)

        except (RuntimeError, TypeError, ValueError):
            mae = np.nan
            rmse = np.nan
            e_max = np.nan
            r2 = np.nan
            mape = np.nan
            n = len(y)

        results.append([mae, rmse, e_max, r2, mape, n])

    names = ['linear', 'quadratic', 'exponential', 'logarithmic', 'logistic']
    metrics = ['MAE', 'RMSE', 'Max_Error', 'R2', 'MAPE', 'N']

    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    dt = pd.DataFrame(results, columns=metrics, index=names)

    return dt