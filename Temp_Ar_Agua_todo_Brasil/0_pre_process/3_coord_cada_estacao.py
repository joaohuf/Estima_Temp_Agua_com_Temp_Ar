import numpy as np
import os
import pandas as pd

# Separa as coordenadas das estacoes com dados de temperatura com base no arquivo f_ests

Dir = '/media/joao/HD-jao/Artigo_Temp_Ar_Agua/Hidroweb/processado/'
Dir_save = '/media/joao/HD-jao/Artigo_Temp_Ar_Agua/Hidroweb/'

f_ests = '/home/joao/Dropbox/Scripts/Python/s3_joao/relacao_estacoes_HidroWeb.txt'

dt = pd.read_csv(f_ests, sep="\t")
dt = dt[dt['Tipo'] == 1]

cods = [f.split('_')[0] for f in os.listdir(Dir)]

dt = dt[dt['Codigo'].isin(cods)]
dt = dt[['Codigo', 'Latitude', 'Longitude']]
dt = dt.set_index('Codigo')

dt_1 = dt.iloc[:2000, :]
dt_2 = dt.iloc[2000:, :]

dt.to_csv(f'{Dir_save}Estacoes_processadas.txt', sep='\t')
dt_1.to_csv(f'{Dir_save}Estacoes_processadas_part_1.txt', sep='\t')
dt_2.to_csv(f'{Dir_save}Estacoes_processadas_part_2.txt', sep='\t')
