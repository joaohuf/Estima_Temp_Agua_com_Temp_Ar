import pandas as pd
import matplotlib.pyplot as plt
import os
import funcoes
from scipy.optimize import curve_fit
import numpy as np

# Gera a série temporal a partir da melhor regressao

def Calc_Temp(function, x, y, x_full):

    try:
        popt, _, = curve_fit(function, x, y)

        if len(popt) == 2:
            a, b = popt
            y_pred = function(x_full, a, b)
        elif len(popt) == 3:
            a, b, c = popt
            y_pred = function(x_full, a, b, c)
        else:
            a, b, c, d = popt
            y_pred = function(x_full, a, b, c, d)

    except (RuntimeError, TypeError, ValueError):
        y_pred = np.nan

    return y_pred

Dir = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Resultados\\'
Dir_T_ar = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Dados_temp\\processado_GEE\\'
Dir_T_agua = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Dados_temp\\processado_hidroweb\\'

Dir_save = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Resultados\\Time_Series\\'

# Dicionário com as cores a serem usadas para cada métrica
# Metrics = ['MAE', 'RMSE', 'Max_Error', 'R2', 'MAPE']
Metrics = ['R2']

base_name = 'Combined'

dt_GEE_NCAR = pd.read_csv(f'{Dir_T_ar}Temp_Ar_NCAR.txt', sep='\t', index_col=0, parse_dates=True)
dt_GEE_CFSV2 = pd.read_csv(f'{Dir_T_ar}Temp_Ar_CFSV2.txt', sep='\t', index_col=0, parse_dates=True)
dt_GEE_ECMWF = pd.read_csv(f'{Dir_T_ar}Temp_Ar_ECMWF.txt', sep='\t', index_col=0, parse_dates=True)

for metric in Metrics:

    dt_regre = pd.read_csv(f"{Dir}best_{metric}_{base_name}.txt", sep='\t', index_col=0)

    for cod, row in dt_regre.iterrows():

        MM = int(row['MM'][2:])
        Func = row['Func']
        Font = row['Fonte']
        N = row['N']

        if N > 3:

            # Abre os dados do GEE
            if Font == 'NCAR':
                dt_GEE = dt_GEE_NCAR[[str(cod)]]
            elif Font == 'CFSV2':
                dt_GEE = dt_GEE_CFSV2[[str(cod)]]
            elif Font == 'ECMWF':
                dt_GEE = dt_GEE_ECMWF[[str(cod)]]

            else:
                print('SEM FONTE DE DADOS')
                exit()

            # Separa uma cópia para depois
            dt = dt_GEE[[str(cod)]].copy()
            dt.columns = ['T_Ar']

            # Faz a média móvel
            dt_GEE = dt_GEE.rolling(window=MM, win_type=None).mean().dropna()
            dt_GEE.columns = ['T_Ar_MM']

            # Abre os dados do hidroweb
            dt_hidroweb = pd.read_csv(f'{Dir_T_agua}{cod}_T_agua.txt', sep='\t', index_col=0, parse_dates=True)
            dt_hidroweb = dt_hidroweb.resample('D').mean()
            dt_hidroweb.columns = ['T_Agua_Hidroweb']

            # Junta T_Agua_Hidroweb e T_Ar_MM, para pegar só os dias onde ambos possuem dados
            dt_pivot = pd.concat([dt_hidroweb, dt_GEE], axis=1).dropna()
            y = dt_pivot['T_Agua_Hidroweb'].values
            x = dt_pivot['T_Ar_MM'].values

            # Função a ser usada na regressão
            full_Func = getattr(funcoes, Func)

            # Calcula o valor ajustado da temperatura da água
            y_pred = Calc_Temp(full_Func, x, y, dt_GEE['T_Ar_MM'].values)

            dt_GEE['T_Agua_GEE'] = y_pred

            # Junta os dados
            dt = pd.concat([dt, dt_GEE], axis=1)
            dt = pd.concat([dt_hidroweb, dt], axis=1).round(2)

            # Salva os resultados
            f_save = f'{Dir_save}Result_{metric}_{base_name}_{cod}.txt'
            dt.to_csv(f_save, sep='\t')