import logging
import pandas as pd
from utils.cfg import CINE_URL, MUSEO_URL, BIBLIOTECA_URL
from utils.data_extractors import MuseumExtractor, CinemaExtractor, LibraryExtractor
import numpy as np

extractors = { 'museum' : MuseumExtractor(MUSEO_URL,'museum'),
               'cinema' :CinemaExtractor(CINE_URL,'cine'),
               'library' : LibraryExtractor(BIBLIOTECA_URL,'biblioteca')}

# Create and configure logger
logging.basicConfig(filename="data_analytics_challenge.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

log = logging.getLogger()
   
    
def extract():
    df_out = {}
    for key, value in extractors.items():
        df_out[key] = value.extract()
    return df_out


def transform(df_extract):
    df_out = {}
    i = 0
    for key, ext in extractors.items():
        df_out[key] = ext.transform(df_extract[key])
        i += 1
    
    return df_out


def load():
    pass

def combined_df(df:pd.DataFrame):
    log.info('Creating total category registers dataframe.')
    df_total_category_registers = df.groupby('categoria',as_index=False).size()
    df_total_category_registers = df_total_category_registers.rename(columns={'size':'total'})
    
    log.info('Creating total category province registers dataframe.')
    df_unified_cat_prov = df.groupby(['categoria','provincia'],as_index=False).size()
    df_unified_cat_prov = df_unified_cat_prov.rename(columns={'size':'total'})
    
    return df_total_category_registers, df_unified_cat_prov


def source_df(dict_df):
    dict_source = {'source': [], 'total':[]}
    
    for key,value in dict_df.items():
        dict_source['source'].append(key)
        dict_source['total'].append(value.size) 

    return pd.DataFrame(dict_source)
    
def cinema_df(df_cinema):
    df_cinema['espacio_INCAA'] = df_cinema['espacio_INCAA'].replace({'0':np.nan})
    dict_cinema_province_sum = df_cinema.groupby(['Provincia'],as_index=False)['Pantallas','Butacas'].sum() 
    dict_cinema_province_count = df_cinema.groupby(['Provincia'],as_index=False)['espacio_INCAA'].count() 
    return pd.concat([dict_cinema_province_sum,dict_cinema_province_count],axis=1)
    


def run_pipeline():
    """Implements ETL process.
    """
    #Extract
    log.info('Extract phase.')
    df_list = extract()
    
    #Transform
    log.info('Transform phase.')
    df_transformed = transform(df_list)
    
    #Merge df
    log.info('Merging dataframes.')
    df_unified = pd.concat(list(df_transformed.values()))

    log.info('Creating total category registers & Category Province dataframes.')
    df_total_category_registers, df_unified_cat_prov = combined_df(df_unified)
    log.info('Creating total source dataframe.')
    df_source = source_df(df_transformed)
    log.info('Creating cinema dataframe.')
    df_cinema = cinema_df(df_list['cinema'])
    
    #Load
    log.info('Load phase.')

    
    log.info('Work done!')
    
    
if __name__ == '__main__':
    log.info('Starting ETL pipeline.')
    run_pipeline()