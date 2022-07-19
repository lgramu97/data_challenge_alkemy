import logging
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from cfg import DB_CONNSTR
from constants import MAIN_TABLE, CINE_TABLE, CATEGORY_REGISTER, SOURCE_REGISTER, CATEGORY_PROV_REGISTER

# Create and configure logger
logging.basicConfig(filename="data_analytics_challenge.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

log = logging.getLogger()
   
engine = create_engine(DB_CONNSTR)

class Loader():
    
    def _load(df:pd.DataFrame,table_name:str):
        df.to_sql(table_name,con=engine, index=False, if_exists='replace')
    
    def load_total_category_registers(self,df:pd.DataFrame):
        log.info('Creating total category registers dataframe.')
        df_total_category_registers = df.groupby('categoria',as_index=False).size()
        df_total_category_registers = df_total_category_registers.rename(columns={'size':'total'})
        self._load(df_total_category_registers,CATEGORY_REGISTER)
       
        
    def load_unified_cat_prov(self,df:pd.DataFrame):
        log.info('Creating total category province registers dataframe.')
        df_unified_cat_prov = df.groupby(['categoria','provincia'],as_index=False).size()
        df_unified_cat_prov = df_unified_cat_prov.rename(columns={'size':'total'})
        self._load(df_unified_cat_prov,CATEGORY_PROV_REGISTER)
        
        
    def load_source_df(self,dict_df):
        log.info('Creating source registers dataframe.')
        dict_source = {'source': [], 'total':[]}
        
        for key,value in dict_df.items():
            dict_source['source'].append(key)
            dict_source['total'].append(value.size) 

        df_source = pd.DataFrame(dict_source)
        self._load(df_source,SOURCE_REGISTER)
    
    
    def load_cinema_df(self,df_cinema):
        log.info('Creating cinema registers dataframe.')
        df_cinema['espacio_INCAA'] = df_cinema['espacio_INCAA'].replace({'0':np.nan})
        dict_cinema_province_sum = df_cinema.groupby(['Provincia'],as_index=False)['Pantallas','Butacas'].sum() 
        dict_cinema_province_count = df_cinema.groupby(['Provincia'],as_index=False)['espacio_INCAA'].count() 
        
        df_cinema_new = pd.concat([dict_cinema_province_sum,dict_cinema_province_count],axis=1)
        self._load(df_cinema_new,CINE_TABLE)