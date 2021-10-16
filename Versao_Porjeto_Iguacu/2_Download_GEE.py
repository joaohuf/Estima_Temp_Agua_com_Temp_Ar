import ee
import geemap
import numpy as np
import pandas as pd
from datetime import datetime as dt
from tqdm import tqdm


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

# Inicializa o Google Earth Engine (GEE)
# Para fazer uso é preciso ter conta no GEE
# ee.Authenticate()
ee.Initialize()

# Onde salvar e prefixo do nome dos arquivos
Dir_save = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\Dados_GEE\\'
f_save = f'{Dir_save}ECMWF'

# Pega as coordenadas a serem usadas no GEE
f_geom = 'E:\\Projeto_Iguacu\\Temp_Ar_Agua\\estacoes_qualidade.txt'
dt_geom = pd.read_csv(f_geom, sep='\t')
dt_geom["Codigo"] = dt_geom["Codigo"].astype('int')

# Transforma o geodataframe no formato que o GEE aceita
points_shp = geemap.pandas_to_ee(dt_geom, latitude="Latitude", longitude="Longitude")

# Anos a serem usados
anos = np.arange(1990, 2020 + 1, 1)

# Itera entre os anos - Isso evita que ocorra o erro TimeOut, por que o GEE limita a quantidade de coisas que podem ser baixadas por vez
for ano in anos:
    begin = f"{ano}-01-02"
    end = f"{ano+1}-01-02"

    # Dataset do GEE a ser usado para pegar os dados meteorológicos
    # Outros datasets podem ser usados como: CFSV2, ...
    # Só trocar o ECMWF/ERA5/DAILY e mean_2m_air_temperature
    dataset = ee.ImageCollection('ECMWF/ERA5/DAILY') \
        .select(['mean_2m_air_temperature']) \
        .filterDate(begin, end) \
        .filterBounds(points_shp) \
        .sort('system:time_start')

    # Clipa o dataset do GEE com as coords das estações de qualidade da água
    dataset = dataset.map(lambda img: img.clip(points_shp))

    # Pega os dados de cada pixel (coordenada)
    pixels_timeserie = pixels_values(dataset, points_shp, "mean_2m_air_temperature", id_name='Codigo')

    # Transforma em dataframe e formata
    dfs = [pd.DataFrame(pt[1], columns=[pt[0].strftime("%Y-%m-%d"), "geom", "id"]) for pt in pixels_timeserie]
    df_concat = pd.concat(dfs, axis=1, join="inner")
    df_concat = df_concat.drop(["geom", "id"], axis=1).T
    df_concat.columns = dt_geom['Codigo'].tolist()

    # Salva os dados
    df_concat.round(2).to_csv(f"{f_save}_{ano}.txt", sep='\t')

    exit()