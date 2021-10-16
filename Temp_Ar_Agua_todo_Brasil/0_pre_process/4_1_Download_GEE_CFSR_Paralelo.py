import ee
import geemap
import numpy as np
import pandas as pd
from datetime import datetime as dt
from tqdm import tqdm
import multiprocessing
import os

# Faz o download dos dados de temperatura do ar do modelo CFSR através do Google Earth Engine

def img_datetime(img):
    imgdate = dt.fromtimestamp(img.get("system:time_start").getInfo() / 1000.)
    return imgdate


def img_ids(imgcollection):
    ids = [item.get('id') for item in imgcollection.getInfo().get('features')]
    return ids


def pixels_values(imgcollection, geometries, band_name, id_name):
    ids_list = img_ids(imgcollection)

    pixel_all_values = []
    for id in tqdm(ids_list):
        image = ee.Image(id).select(band_name)

        image_pixels = image.reduceRegions(
            reducer=ee.Reducer.mean(),
            collection=geometries,
            # scale=9999,
        )
        # .filter(ee.Filter.neq('mean', None))

        img_date = img_datetime(image)
        values = []
        for pixel in image_pixels.getInfo()['features']:
            geom = pixel['geometry']['coordinates']
            pixel_id = pixel['properties'][id_name]

            try:
                mean = pixel['properties']['mean']
            except:
                mean = -999

            values.append([mean, geom, pixel_id])
            # values.append([img_date, mean, geom])

        pixel_all_values.append([img_date, values])
        # pixel_all_values.append(values)

    return pixel_all_values


def Run_all(dates):
    star_year = dates[0][0]
    start_month = dates[0][1]

    end_year = dates[1][0]
    end_month = dates[1][1]

    begin = f"{star_year}-{start_month}-02"
    end = f"{end_year}-{end_month}-02"

    dataset = ee.ImageCollection('NOAA/CFSV2/FOR6H') \
        .select(['Temperature_height_above_ground']) \
        .filterDate(begin, end) \
        .filterBounds(points_shp) \
        .sort('system:time_start')

    dataset = dataset.map(lambda img: img.clip(points_shp))
    pixels_timeserie = pixels_values(dataset, points_shp, "Temperature_height_above_ground", id_name='Codigo')

    dfs = [pd.DataFrame(pt[1], columns=[pt[0].strftime("%Y-%m-%d"), "geom", "id"]) for pt in pixels_timeserie]
    df_concat = pd.concat(dfs, axis=1, join="inner")
    df_concat = df_concat.drop(["geom", "id"], axis=1).T
    df_concat.columns = dt_geom['Codigo'].tolist()

    df_concat.round(2).to_csv(f"{f_save}_{star_year}_{start_month}.txt", sep='\t')


# Na primeira vez é necessário autenticar o computador
# ee.Authenticate()
ee.Initialize()

# Onde salvar e prefixo do nome dos arquivos
Dir_save = 'E:\\Artigos\\Artigo_Temp_Ar_Agua\\Dados_temp\\Bruto_GEE\\CFSV2\\'
part = 'A'
f_save = f'{Dir_save}CFSV2_{part}'

f_geom = "E:\\Artigos\\Artigo_Temp_Ar_Agua\\Dados_temp\\Estacoes_processadas.txt"
dt_geom = pd.read_csv(f_geom, sep='\t')
dt_geom["Codigo"] = dt_geom["Codigo"].astype('int')

# O GEE apresenta um limite na quantidade de dados que podem ser baixados ao mesmo tempo
# Por isso as vezes é necessário fazer o download por partes

# dt_geom = dt_geom.iloc[:2500, :]

points_shp = geemap.pandas_to_ee(dt_geom, latitude="Latitude", longitude="Longitude")

list_dates = pd.date_range('1990-01', '2020-02', freq='6M').strftime("%Y-%m").tolist()
list_dates = np.array([[list_dates[i].split('-'), list_dates[i+1].split('-')] for i in range(len(list_dates)-1)]).astype('int')
list_dates = list_dates.tolist()

# Pega o mes e ano rodado
dates_rodados = [[int(f.split('_')[-2]), int(f.split('_')[-1][:-4])] for f in os.listdir(Dir_save) if part in f.split('_')[-3]]

# Seleciona os anos que não foram rodadas
list_dates = [date for date in list_dates if not date[0] in dates_rodados]

N_processos = 1

if __name__ == '__main__':
    # Cria as pools pra rodar em paralelo
    pool = multiprocessing.Pool(processes=N_processos)
    pool.map(Run_all, list_dates)
