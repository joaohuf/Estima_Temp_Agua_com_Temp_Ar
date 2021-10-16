import pandas as pd
import matplotlib.pyplot as plt
import os

# Plota a serie temporal

Dir = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Resultados\\'
Dir_save = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Graficos\\Time_Series\\'

# Dicionário com as cores a serem usadas para cada métrica
Dic = {'MAE': 'dodgerblue',
       'RMSE': 'orangered',
       'Max_Error': 'seagreen',
       'R2': 'crimson',
       'MAPE': 'purple'}

for f in os.listdir(f'{Dir}Time_Series\\'):
    print(f)
    # Pega a métrica, código da estação e cor a ser usada
    metric = f.split('_')[1]
    tipo = f.split('_')[2]
    cod = f.split('_')[-1][:-4]
    cor = Dic[metric]

    # Abre os dados
    dt = pd.read_csv(f'{Dir}Time_Series\\{f}', sep='\t', index_col=0, parse_dates=True)[['T_Agua_Hidroweb', 'T_Agua_GEE']]
    metric_value, N_samples = pd.read_csv(f'{Dir}best_{metric}_{tipo}.txt', sep='\t', index_col=0, parse_dates=True).loc[int(cod)][[metric, 'N']].tolist()

    # Plota a série histórica ajustada e observada
    fig, ax = plt.subplots(figsize=(8, 5))
    dt['T_Agua_GEE'].plot(ax=ax, color=cor, label='Regressão')
    dt['T_Agua_Hidroweb'].plot(ax=ax, color='black', marker='o', ms=4, label='Medido', ls='')

    # Formatação e salva a figura
    plt.xlabel('Data')
    plt.ylabel('Temperatura da Água (C°)')
    plt.title(f'Estação: {cod}\nMelhor ajuste: {metric} = {metric_value}, N = {N_samples}')
    plt.legend()
    plt.tight_layout()

    plt.savefig(f'{Dir_save}Time_series_{metric}_{cod}.png', format='png', dpi=300)
    plt.close()