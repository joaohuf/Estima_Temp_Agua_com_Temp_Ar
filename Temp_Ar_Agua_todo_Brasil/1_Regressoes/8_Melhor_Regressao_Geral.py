import pandas as pd

# Pega a melhor regresso considerando todos os modelos meteorologicos

# Local onde estão os dados e onde salvar
Dir = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Resultados\\'

# Metricas que foram feitas
Metrics = ['MAE', 'RMSE', 'Max_Error', 'R2', 'MAPE']

# Itera as métricas - Gera um arquivo resumo para cada métrica
for metric in Metrics:
    print(metric)
    # Itera as estações

    dt_ECMWF = pd.read_csv(f'{Dir}best_{metric}_ECMWF.txt', index_col=0, sep='\t')
    dt_ECMWF['Fonte'] = 'ECMWF'

    dt_CFSV2 = pd.read_csv(f'{Dir}best_{metric}_CFSV2.txt', index_col=0, sep='\t')
    dt_CFSV2['Fonte'] = 'CFSV2'

    dt_NCAR = pd.read_csv(f'{Dir}best_{metric}_NCAR.txt', index_col=0, sep='\t')
    dt_NCAR['Fonte'] = 'NCAR'

    dt_resume = pd.concat([dt_ECMWF, dt_CFSV2, dt_NCAR], axis=0)
    dt_resume.index.name = 'Cod'

    if metric != 'R2':
        dt_resume = dt_resume.sort_values(by=[metric, 'Cod'], ascending=True)
    else:
        dt_resume = dt_resume.sort_values(by=[metric, 'Cod'], ascending=False)

    dt_resume = dt_resume[~dt_resume.index.duplicated(keep='first')]
    dt_resume = dt_resume.sort_index()

    dt_resume.to_csv(f'{Dir}best_{metric}_Combined.txt', sep='\t')