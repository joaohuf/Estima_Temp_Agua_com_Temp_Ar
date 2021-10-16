import pandas as pd
from s3_joao import io
import os
import numpy as np

# Faz o download dos dados bruto de qualidade da água do hidroweb


Dir = '/media/joao/HD-jao/Artigo_Temp_Ar_Agua/Dados_temp/bruto_hidroweb/'
f_ests = '/home/joao/Dropbox/Scripts/Python/s3_joao/relacao_estacoes_HidroWeb.txt'
est_baixadas = '/media/joao/HD-jao/Artigo_Temp_Ar_Agua/Dados_temp/est_baixadas.txt'

tipo_esp = 'qualagua'

dt = pd.read_csv(f_ests, sep="\t")
dt = dt[dt['Tipo'] == 1]

if os.path.isfile(est_baixadas):
    dt_executados = pd.read_csv(est_baixadas, sep='\t', index_col=0)
else:
    dt_executados = pd.DataFrame()
    dt_executados['Codigo'] = np.nan

cods_nao_rodados = []
for cod in dt['Codigo'].tolist():
    if cod not in dt_executados['Codigo'].values:
        cods_nao_rodados.append(cod)

for cod in cods_nao_rodados:
    io.download_station(cod, formato=2, dir=Dir, tipo_especifico='qualagua', save_zip=False)
    dt_executados.loc[dt_executados.shape[0]] = str(cod)
    dt_executados.to_csv(est_baixadas, sep='\t')
