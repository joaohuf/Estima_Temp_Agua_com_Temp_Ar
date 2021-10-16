import numpy as np
import pandas as pd
from funcoes import best_regression

# Local onde estão os dados e onde salvar
Dir = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Dados\\'
Dir_save = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Analise\\'

# Arquivo com as coordenadas
f_coords = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\estacoes_qualidade.txt'
cods = pd.read_csv(f_coords, sep='\t')['Codigo'].tolist()

# Itera entre cada coordenada
for cod in cods:
    print(cod)

    # Arquivo de dados do hidroweb
    f_hidroweb = f'{Dir}hidroweb_{cod}.txt'
    dt_hidroweb = pd.read_csv(f_hidroweb, sep='\t', index_col=0, parse_dates=True)
    dt_hidroweb.columns = ['Hidroweb']

    # Arquivo de dados do GEE
    f_GEE = f'{Dir}ECMWF_{cod}.txt'
    dt_GEE = pd.read_csv(f_GEE, sep='\t', index_col=0, parse_dates=True)
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
        dt_results = best_regression(x, y)

        # Adiciona um novo index pra juntar tudo depois
        new_index = pd.MultiIndex.from_product([['MM'+str(i)], dt_results.index.tolist()], names=['MM', 'Func'])
        dt_results.index = new_index

        # Guarda os dados para cada iteração
        list_results.append(dt_results)

    # Junta e salva os resultados
    dt_results = pd.concat(list_results).round(2)
    dt_results.to_csv(f'{Dir_save}ECMWF_{cod}.txt', sep='\t')