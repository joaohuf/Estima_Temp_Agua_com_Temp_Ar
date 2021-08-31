import pandas as pd
import matplotlib.pyplot as plt
import os

Dir = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Dados_Regressoes\\'
Dir_save = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Plots\\'

# Dicionário com as cores a serem usadas para cada métrica
Dic = {'MAE': 'dodgerblue',
       'RMSE': 'orangered',
       'Max_Error': 'seagreen',
       'R2': 'crimson',
       'MAPE': 'purple'}

for f in os.listdir(Dir):
    # Pega a métrica, código da estação e cor a ser usada
    metric = f[7:-13]
    cod = f[-12:-4]
    cor = Dic[metric]

    # Abre os dados
    dt = pd.read_csv(f'{Dir}{f}', sep='\t', index_col=0, parse_dates=True)[['T_Agua_Hidroweb', 'T_Agua_GEE']]

    # Plota a série histórica ajustada e observada
    fig, ax = plt.subplots(figsize=(12, 5))
    dt['T_Agua_GEE'].plot(ax=ax, color=cor, label='Regressão')
    dt['T_Agua_Hidroweb'].plot(ax=ax, color='black', marker='o', ms=4, label='Medido', ls='')

    # Formatação e salva a figura
    plt.xlabel('Data')
    plt.ylabel('Temperatura do Ar (C°)')
    plt.title(f'Melhor ajuste usando: {metric}')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{Dir_save}Time_series_{metric}_{cod}.png', format='png', dpi=300)
    plt.close()
