import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Plota os resultados por métrica

# Diretório com a análise resumo e onde salvar
Dir = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Resultados\\'
Dir_save = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Graficos\\'

base_names = ['ECMWF', 'CFSV2', 'NCAR', 'Combined']

# Métricas e cores a serem usadas
pars = ['MAE', 'RMSE', 'Max_Error', 'R2', 'MAPE']
colors = ['dodgerblue', 'orangered', 'seagreen', 'crimson', 'purple']
limits = [[-0.01, 5], [-0.01, 5], [-0.01, 10], [-0.01, 1.01], [-0.01, 1]]

for par, cor, limit in zip(pars, colors, limits):
    list_dts = []
    for base_name in base_names:
        f = f'{Dir}best_{par}_{base_name}.txt'
        # Abre os resultados dos ajustes
        dt = pd.read_csv(f, sep='\t', index_col=0)[['MM', par]]
        dt = dt[[par]]
        dt.columns = [base_name]

        list_dts.append(dt)

    # Cria um dataframe com os melhores resultados para cada métrica
    # dt = pd.concat(list_dts, axis=1)
    dt = pd.concat(list_dts, axis=1).melt(var_name='Source', value_name='Value')

    # Faz o boxplot das métricas
    ax = sns.boxplot(x="Source", y="Value", data=dt, zorder=1, color=cor)
    ax.set_ylim(limit)

    # Formatação e salva a figura
    ax.set_axisbelow(True)
    ax.grid(axis='y', color='gray')
    plt.title(par)
    plt.tight_layout()
    plt.savefig(f'{Dir_save}Boxplot_metric_{par}.png', format='png', dpi=300)
    plt.close()
