import numpy as np
import pandas as pd
from funcoes import best_regression
import os

# Aplica as regressoes para cada estacao

# Local onde estão os dados e onde salvar
Dir = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Dados_temp\\'
Dir_save = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Regressoes\\'
base_name = 'ECMWF'
# base_name = 'CFSV2'
# base_name = 'NCAR'

f_GEE = f'{Dir}processado_GEE\\Temp_Ar_{base_name}.txt'
dt_GEE_geral = pd.read_csv(f_GEE, sep='\t', index_col=0, parse_dates=True)

# Arquivo com as coordenadas
files_Hidroweb = os.listdir(f'{Dir}processado_hidroweb\\')

# Itera entre cada coordenada
for cod in dt_GEE_geral.columns.tolist():
    print(cod)

    # Arquivo de dados do hidroweb
    f_hidroweb = f"{Dir}processado_hidroweb\\{cod}_T_agua.txt"

    dt_hidroweb = pd.read_csv(f_hidroweb, sep='\t', index_col=0, parse_dates=True)
    dt_hidroweb = dt_hidroweb.resample('D').mean()
    dt_hidroweb.columns = ['Hidroweb']

    # Arquivo de dados do GEE
    dt_GEE = dt_GEE_geral[[cod]]
    dt_GEE.columns = ['GEE']

    # Itera para fazer a média móvel entre 1 e 30 dias
    list_results = []
    for i in np.arange(1, 30 + 1, 1):
        # Aplica a média móvel
        dt_MM = dt_GEE.rolling(window=i, win_type=None).mean()

        # Junta os dados medidos de temp da água e Média Móvel (MM)
        dt_pivot = pd.concat([dt_hidroweb, dt_MM], axis=1).dropna()

        dt_pivot.columns = ['T_Agua', 'T_Ar_MM']

        # Aplica as regressões e retorna os resultados
        y = dt_pivot['T_Agua'].values
        x = dt_pivot['T_Ar_MM'].values

        if len(y) > 3:
            dt_results = best_regression(x, y)
        else:
            names = ['linear', 'quadratic', 'exponential', 'logarithmic', 'logistic']
            metrics = ['MAE', 'RMSE', 'Max_Error', 'R2', 'MAPE', 'N']
            dt_results = pd.DataFrame(columns=metrics, index=names)
            dt_results['N'] = len(y)

        # Adiciona um novo index pra juntar tudo depois
        new_index = pd.MultiIndex.from_product([[str(i)], dt_results.index.tolist()], names=['MM', 'Func'])
        dt_results.index = new_index

        # Guarda os dados para cada iteração
        list_results.append(dt_results)

    # Junta e salva os resultados
    dt_results = pd.concat(list_results).round(2)
    dt_results.to_csv(f'{Dir_save}{base_name}_{cod}.txt', sep='\t')
