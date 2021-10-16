import pandas as pd

# Arquivo com as coordenadas dos arquivos de qualidade da água
f_coords = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\estacoes_qualidade.txt'

# Arquivos onde estão os dados processados pelo Projeto Iguaçu e onde salva os dados processados
dir_quali = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Qualidade\\'
dir_save = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Dados\\'

# Abre o arquivos com os códigos e coordenadas
dt_coords = pd.read_csv(f_coords, sep='\t', index_col=0)

for cod in dt_coords.index:
    print(cod)

    # Abre o arquivo pre-processado
    f_quali = f'{dir_quali}qualagua_T_{cod}.txt'

    # Separa só os dados de temperatura da água
    dt = pd.read_csv(f_quali, sep='\t', index_col=0, parse_dates=True)
    dt = dt[['T_Amostra']]

    # Faz a média diária
    dt = dt.resample('D').mean().dropna()

    # Salva os novos arquivos processados
    f_save = f'{dir_save}hidroweb_{cod}.txt'
    dt.to_csv(f_save, sep='\t')