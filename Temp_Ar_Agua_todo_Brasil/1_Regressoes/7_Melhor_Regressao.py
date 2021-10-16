import pandas as pd

# Separa a melhor regressao por metrica, modelo meteorologico e estacao

# Local onde estão os dados e onde salvar
Dir = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Regressoes\\'
Dir_save = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Resultados\\'
base_name = 'ECMWF'
# base_name = 'CFSV2'
# base_name = 'NCAR'

f_est = "E:\\Artigos\\Artigo_Temp_Ar_Agua\\Dados_temp\\Estacoes_processadas.txt"
dt = pd.read_csv(f_est, sep='\t', index_col=0)

# Metricas que foram feitas
Metrics = ['MAE', 'RMSE', 'Max_Error', 'R2', 'MAPE']

# Itera as métricas - Gera um arquivo resumo para cada métrica
for metric in Metrics:
    print(metric)
    # Itera as estações
    list_dts = []
    for cod in dt.index.values:
        print(cod)
        # Separa a média móvel e função com o melhor resultado
        dt_results = pd.read_csv(f'{Dir}{base_name}_{cod}.txt', sep='\t')
        if metric != 'R2':
            dt_results = dt_results.sort_values(by=metric, ascending=True).iloc[:1, :]
        else:
            dt_results = dt_results.sort_values(by=metric, ascending=False).iloc[:1, :]

        dt_results.index = [cod]

        list_dts.append(dt_results)

    # Junta e salva os resultados
    dt_resume = pd.concat(list_dts, axis=0)
    dt_resume = pd.concat([dt_resume, dt], axis=1)

    dt_resume.to_csv(f'{Dir_save}best_{metric}_{base_name}.txt', sep='\t')