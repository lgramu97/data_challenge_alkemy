from datetime import datetime
import logging
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from utils.cfg import DB_CONNSTR
from utils.constants import MAIN_TABLE, CINE_TABLE, CATEGORY_REGISTER, SOURCE_REGISTER, CATEGORY_PROV_REGISTER
import psycopg2.extras as extras
import psycopg2


# Create and configure logger
logging.basicConfig(filename="data_analytics_challenge.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

log = logging.getLogger()
   
engine = create_engine(DB_CONNSTR)


class Loader():
    
    table_name = MAIN_TABLE
    
    def load(self, df):
        #df to sql creates the  table and replace data if exists.
        df.to_sql(self.table_name,con=engine, index=False, if_exists='replace')
        #Another way is to insert manually data.
        """
        job_date =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df['job_date'] = job_date
        
        tuples = [tuple(x) for x in df.to_numpy()]
        cols = ','.join(list(df.columns))
        
        # SQL query to execute
        query = "INSERT INTO %s(%s) VALUES %%s" % (self.table_name, cols)
        connection = engine.raw_connection()
        cursor = connection.cursor()
        try:
            extras.execute_values(cursor, query, tuples)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            print(query)
            print("tuples: ",tuples)
            connection.rollback()
            cursor.close()
            return 1
        log.info("the dataframe is inserted")
        cursor.close()
        """
    
    
class LoadTotalCategoryRegisters(Loader):
    
    table_name = CATEGORY_REGISTER
    
    def load(self,df:pd.DataFrame):
        log.info('Creating total category registers dataframe.')
        df_total_category_registers = df.groupby('categoria',as_index=False).size()
        df_total_category_registers = df_total_category_registers.rename(columns={'size':'total'})
        super().load(df_total_category_registers)
       
        
class LoadUnifiedCatProv(Loader):
    
    table_name = CATEGORY_PROV_REGISTER

    def load(self,df):
        log.info('Creating total category province registers dataframe.')
        df_unified_cat_prov = df.groupby(['categoria','provincia'],as_index=False).size()
        df_unified_cat_prov = df_unified_cat_prov.rename(columns={'size':'total'})
        super().load(df_unified_cat_prov)
        
        
class LoadSource(Loader):
    
    table_name = SOURCE_REGISTER
    
    def load(self, df):
        """Create total source dataframe.

        Args:
            df (dictionary): dictionary with source and df.
        """
        log.info('Creating source registers dataframe.')
        dict_source = {'source': [], 'total':[]}
        
        for key,value in df.items():
            dict_source['source'].append(key)
            dict_source['total'].append(value.size) 

        df_source = pd.DataFrame(dict_source)
        super().load(df_source)

    
class LoadCinema(Loader):
    
    table_name = CINE_TABLE
    
    def _rename(self,df:pd.DataFrame)-> pd.DataFrame:
        col_rename = {
            'Provincia':'provincia',
            'Pantallas':'cantidad_pantallas',
            'Butacas':'cantidad_butacas',
            'espacio_INCAA' : 'cantidad_incaa'
        }
        return df.rename(columns=col_rename, inplace = True)
    
    def load(self, df):
        log.info('Creating cinema registers dataframe.')
        df['espacio_INCAA'] = df['espacio_INCAA'].replace({'0':np.nan})
        
        dict_cinema_province_sum = df.groupby(['Provincia'],as_index=False)['Pantallas','Butacas'].sum() 
        dict_cinema_province_count = df.groupby(['Provincia'],as_index=False)['espacio_INCAA'].count() 

        df_cinema_concat = dict_cinema_province_sum.join(dict_cinema_province_count.set_index('Provincia'),on='Provincia')
        #df_cinema_concat.replace(np.nan, 0, inplace=True)

        self._rename(df_cinema_concat)
        return super().load(df_cinema_concat)    
