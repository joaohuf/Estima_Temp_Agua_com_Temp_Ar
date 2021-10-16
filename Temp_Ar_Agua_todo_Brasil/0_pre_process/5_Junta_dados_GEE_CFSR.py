import pandas as pd
import os
import numpy as np

# Reorganiza os dados do modelo CFSR baixados do GEE
# Os dados para o Brasil foram baixados em duas partes, separadas em "A" e "B"
# Tomar cuidado com isso e fazer adaptaçoes para cada caso

Dir = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Dados_temp\\Bruto_GEE\\CFSV2\\'
Dir_save = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Dados_temp\\processado_GEE\\'

Kelvin_to_Celcius = 273.15

files = os.listdir(Dir)

files_A = [f for f in files if '_A_' in f]
files_B = [f for f in files if '_B_' in f]

list_dts = []
for f in files_A:
    print(f)
    dt = pd.read_csv(f'{Dir}{f}', sep='\t', index_col=0)
    dt.index = pd.to_datetime(dt.index, format='%Y/%m/%d')
    list_dts.append(dt)

dt_A = pd.concat(list_dts, axis=0).resample('D').mean()

list_dts = []
for f in files_B:
    print(f)
    dt = pd.read_csv(f'{Dir}{f}', sep='\t', index_col=0)
    dt.index = pd.to_datetime(dt.index, format='%Y/%m/%d')
    list_dts.append(dt)

dt_B = pd.concat(list_dts, axis=0).resample('D').mean()

dt = pd.concat([dt_A, dt_B], axis=1)
dt = dt - Kelvin_to_Celcius

mask = (dt > 999)
dt[mask] = np.nan

dt.to_csv(f'{Dir_save}Temp_Ar_CFSV2.txt', sep='\t')
