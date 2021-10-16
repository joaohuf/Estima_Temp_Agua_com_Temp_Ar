import ee
import geemap
import numpy as np
import pandas as pd
from datetime import datetime as dt
from tqdm import tqdm
import multiprocessing


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


def Run_all(start_year):
    print(start_year)
    begin = f"{start_year}-01-02"
    end = f"{start_year + 1}-01-02"

    dataset = ee.ImageCollection('ECMWF/ERA5/DAILY') \
        .select(['mean_2m_air_temperature']) \
        .filterDate(begin, end) \
        .filterBounds(points_shp) \
        .sort('system:time_start')

    dataset = dataset.map(lambda img: img.clip(points_shp))
    pixels_timeserie = pixels_values(dataset, points_shp, "mean_2m_air_temperature", id_name='Codigo')

    dfs = [pd.DataFrame(pt[1], columns=[pt[0].strftime("%Y-%m-%d"), "geom", "id"]) for pt in pixels_timeserie]
    df_concat = pd.concat(dfs, axis=1, join="inner")
    df_concat = df_concat.drop(["geom", "id"], axis=1).T
    df_concat.columns = dt_geom['Codigo'].tolist()

    df_concat.round(2).to_csv(f"{f_save}_{start_year}.txt", sep='\t')

# SEGUE OS MESMOS COMENTÁRIOS DA VERSÃO NÃO EM PARALELA
# ee.Authenticate()
ee.Initialize()

# Onde salvar e prefixo do nome dos arquivos
Dir_save = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Dados_GEE\\'
f_save = f'{Dir_save}ECMWF'

anos_completos = [int(f[6:-4]) for f in os.listdir('E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Dados_GEE\\')]

f_geom = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\estacoes_qualidade.txt'
dt_geom = pd.read_csv(f_geom, sep='\t')
dt_geom["Codigo"] = dt_geom["Codigo"].astype('int')

points_shp = geemap.pandas_to_ee(dt_geom, latitude="Latitude", longitude="Longitude")

anos = np.arange(1980, 2020 + 1, 1)

anos = [ano for ano in anos if ano not in anos_completos]

# N_processos pode ser maior que o número de processadores do seu computador
# O que normalmente limita o download é a taxa de transferência do GEE
N_processos = 20

if __name__ == '__main__':

    # Cria as pools pra rodar em paralelo
    pool = multiprocessing.Pool(processes=N_processos)
    pool.map(Run_all, anos)
