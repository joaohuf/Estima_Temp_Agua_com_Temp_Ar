import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Diretório com a análise resumo e onde salvar
Dir = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Analise_Resume\\'
Dir_save = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Plots\\'

# Métricas e cores a serem usadas
pars = ['MAE', 'RMSE', 'Max_Error', 'R2', 'MAPE']
colors = ['dodgerblue', 'orangered', 'seagreen', 'crimson', 'purple']

list_dts = []
for par, cor in zip(pars, colors):
    f = f'{Dir}best_{par}.txt'

    # Abre os resultados dos ajustes
    dt = pd.read_csv(f, sep='\t', index_col=0)[['MM', par]]

    list_dts.append(dt[[par]])

    # Formatação
    dt.index = dt.index.astype('str')
    # Formatação
    dt['MM'] = dt['MM'].str.replace('MM', '').astype('int')

    # Cria o lugar para plotar
    fig, ax1 = plt.subplots(figsize=(15, 5))
    # Cria um segundo eixo y
    ax2 = ax1.twinx()

    # Plota as métricas e quantos dias de MM foram usados
    dt[par].plot(kind='bar', color=cor, width=0.8, ax=ax1, label=par)
    dt['MM'].plot(kind='line', color='black', ax=ax2, label='MM')

    # Formatação e salva a figura
    ax1.set_xlabel('Código da Estação')
    ax1.set_ylabel(par, color=cor)
    ax2.set_ylabel('Média Móvel', color='black')
    ax1.tick_params(axis='x', labelrotation=90, labelsize=6)
    ax1.tick_params(axis='y', labelcolor=cor)
    ax2.tick_params(axis='y', labelcolor='black')
    plt.tight_layout()
    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)
    plt.savefig(f'{Dir_save}{par}_geral.png', format='png', dpi=300)
    plt.close()

# Cria um dataframe com os melhores resultados para cada métrica
dt = pd.concat(list_dts, axis=1).melt(var_name='Metric', value_name='Value')

# Faz o boxplot das métricas
ax = sns.boxplot(x="Metric", y="Value", data=dt, zorder=1)
ax.set_ylim(0, 10)

# Formatação e salva a figura
ax.set_axisbelow(True)
ax.grid(axis='y', color='gray')
plt.yticks(np.arange(0, 10 + 1, 1.0))
plt.tight_layout()
plt.savefig(f'{Dir_save}Boxplot_geral.png', format='png', dpi=300)
plt.close()