import pandas as pd
import funcoes
from scipy.optimize import curve_fit
import numpy as np

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


# Diretórios onde estão os dados, resumo das análises e onde salvar
Dir = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Analise_Resume\\'
Dir_data = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Dados\\'
Dir_save = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Dados_Regressoes\\'

# Métricas avaliadas
Metrics = ['MAE', 'RMSE', 'Max_Error', 'R2', 'MAPE']

for metric in Metrics:
    # Abre os resultados das regresões
    dt_resume = pd.read_csv(f'{Dir}best_{metric}.txt', sep='\t', index_col=0)

    for cod, row in dt_resume.iterrows():
        # Pega a função de ajuste e a quantidade de dias na média móvel
        MM = int(row['MM'][2:])
        Func = row['Func']

        # Abre os dados do GEE
        dt_GEE = pd.read_csv(f'{Dir_data}ECMWF_{cod}.txt', sep='\t', index_col=0, parse_dates=True)

        # Separa uma cópia para depois
        dt = dt_GEE[[str(cod)]].copy()
        dt.columns = ['T_Ar']

        # Faz a média móvel
        dt_GEE = dt_GEE.rolling(window=MM, win_type=None).mean().dropna()
        dt_GEE.columns = ['T_Ar_MM']

        # Abre os dados do hidroweb
        dt_hidroweb = pd.read_csv(f'{Dir_data}hidroweb_{cod}.txt', sep='\t', index_col=0, parse_dates=True)
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
        f_save = f'{Dir_save}Result_{metric}_{cod}.txt'
        dt.to_csv(f_save, sep='\t')