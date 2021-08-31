import pandas as pd
import os

# Arquivo onde com as coordenadas das estações
f_geral = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\relacao_estacoes_HidroWeb.txt'

# Diretório onde estão os dados de qualidade da água separados pela rotina do Projeto Iguaçu
# https://github.com/UFPR-PPGERHA/Projeto_iguacu
dir_quali = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Qualidade\\'

# Local onde salva o arquivo com as coordenadas dos dados dentro da pasta dei_quali
dir_save = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\'

# Abre o arquivo geral de coordenadas
dt_coords = pd.read_csv(f_geral, sep='\t')

# Pega os códigos das estações
cods = [int(f.replace('qualagua_T_', '')[:-4]) for f in os.listdir(dir_quali) if 'qualagua_T_' in f]

# Separa só as coordenadas dos arquivos na pasta dir_quali
dt_coords = dt_coords[dt_coords['Codigo'].isin(cods)]

# Deixa só latitude e longitude
dt_coords = dt_coords[['Codigo', 'Latitude', 'Longitude']]

# Salva os resultados
dt_coords.to_csv(f'{dir_save}estacoes_qualidade.txt', sep='\t', index=False)