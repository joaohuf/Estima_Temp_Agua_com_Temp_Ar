import pandas as pd
import os

# Locais onde esta os dados do GEE e onde salvar
Dir = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Dados_GEE\\'
Dir_save = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Dados\\'

# Arruma a escala, pois os dados do GEE estão em grau Kelvin e não em grau Celsius
Kelvin_to_Celcius = 273.15

# Coloca todos os dados em formato dataframe e dentro de uma lista
list_dts = [pd.read_csv(f'{Dir}{f}', sep='\t', index_col=0, parse_dates=True) for f in os.listdir(Dir)]

# Junta todos em um dataframe único
dt = pd.concat(list_dts, axis=0)

# Arruma a escala
dt -= Kelvin_to_Celcius

for cod in dt.columns:

    # Confere a escala e gera um arquivo por coluna
    dt_pivot = dt[cod].resample('D').mean().round(2)
    # Salva os dados
    dt_pivot.to_csv(f'{Dir_save}ECMWF_{cod}.txt', sep='\t')
