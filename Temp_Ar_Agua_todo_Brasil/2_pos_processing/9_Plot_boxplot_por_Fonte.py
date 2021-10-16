import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Plota os resultados por fonte de dados temperatura do ar

# Diretório com a análise resumo e onde salvar
Dir = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Resultados\\'
Dir_save = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Graficos\\'

base_names = ['ECMWF', 'CFSV2', 'NCAR', 'Combined']

# Métricas e cores a serem usadas
pars = ['MAE', 'RMSE', 'Max_Error', 'R2', 'MAPE']

Dic = {'MAE': 'dodgerblue',
       'RMSE': 'orangered',
       'Max_Error': 'seagreen',
       'R2': 'crimson',
       'MAPE': 'purple'}

for base_name in base_names:
    list_dts = []
    for par in pars:
        f = f'{Dir}best_{par}_{base_name}.txt'
        # Abre os resultados dos ajustes
        dt = pd.read_csv(f, sep='\t', index_col=0)[['MM', par]]
        list_dts.append(dt[[par]])

    # Cria um dataframe com os melhores resultados para cada métrica
    dt = pd.concat(list_dts, axis=1).melt(var_name='Metric', value_name='Value')

    # Faz o boxplot das métricas
    ax = sns.boxplot(x="Metric", y="Value", data=dt, zorder=1, palette=Dic)
    ax.set_ylim(-0.01, 10)

    # Formatação e salva a figura
    ax.set_axisbelow(True)
    ax.grid(axis='y', color='gray')
    plt.title(base_name)
    plt.yticks(np.arange(0, 10 + 1, 1.0))
    plt.tight_layout()
    plt.savefig(f'{Dir_save}Boxplot_source_{base_name}.png', format='png', dpi=300)
    plt.close()