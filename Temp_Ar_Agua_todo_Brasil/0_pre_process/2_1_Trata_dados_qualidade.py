import os
import numpy as np
from s3_joao.io import Dataframe_from_txt_Hidroweb_QUALIDADE

# Trata e separa só os dados de temperatura da água dos arquivos de qualidade

# A rotina Dataframe_from_txt_Hidroweb_QUALIDADE pode se encontra em
# https://github.com/joaohuf/Ferramentas_HidroWeb/blob/main/hidroweb_files_to_dataframe.py


Dir = '/media/joao/HD-jao/Artigo_Temp_Ar_Agua/Hidroweb/bruto/'
Dir_save = '/media/joao/HD-jao/Artigo_Temp_Ar_Agua/Hidroweb/processado/'

files = os.listdir(Dir)

for i, f in enumerate(files):
    print(f'{i} de {len(files)}, {f}')
    cod = f.split('_')[-1][:-4]

    dt = Dataframe_from_txt_Hidroweb_QUALIDADE(f'{Dir}{f}')
    dt = dt[['T_Amostra']].dropna()
    if not dt.empty:
        dt.to_csv(f'{Dir_save}{cod}_T_agua.txt', sep='\t')