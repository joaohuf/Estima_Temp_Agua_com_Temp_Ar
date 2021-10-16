import pandas as pd

# Local onde estão os dados e onde salvar
Dir = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Analise\\'
Dir_save = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Analise_Resume\\'

f_est = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\estacoes_qualidade.txt'
dt = pd.read_csv(f_est, sep='\t', index_col=0)

# Metricas que foram feitas
Metrics = ['MAE', 'RMSE', 'Max_Error', 'R2', 'MAPE']

# Itera as métricas - Gera um arquivo resumo para cada métrica
for metric in Metrics:

    # Itera as estações
    list_dts = []
    for cod in dt.index.values:
        # Separa a média móvel e função com o melhor resultado
        dt_results = pd.read_csv(f'{Dir}ECMWF_{cod}.txt', sep='\t')
        if metric != 'R2':
            dt_results = dt_results.sort_values(by=metric, ascending=True).iloc[:1, :]
        else:
            dt_results = dt_results.sort_values(by=metric, ascending=False).iloc[:1, :]

        dt_results.index = [cod]

        list_dts.append(dt_results)

    # Junta e salva os resultados
    dt_resume = pd.concat(list_dts, axis=0)
    dt_resume.to_csv(f'{Dir_save}best_{metric}.txt', sep='\t')