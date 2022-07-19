import logging
import pandas as pd
from utils.cfg import CINE_URL, MUSEO_URL, BIBLIOTECA_URL
from utils.data_extractors import MuseumExtractor, CinemaExtractor, LibraryExtractor
from utils.data_load import LoadCinema,LoadSource,LoadTotalCategoryRegisters,LoadUnifiedCatProv, Loader

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

    #Load
    log.info('Load phase.')
    LoadCinema().load(df_list['cinema'])
    LoadSource().load(df_transformed)
    LoadTotalCategoryRegisters().load(df_unified)
    LoadUnifiedCatProv().load(df_unified)
    Loader().load(df_unified)
    log.info('Work done!')
    
    
if __name__ == '__main__':
    log.info('Starting ETL pipeline.')
    run_pipeline()