from abc import  abstractmethod
import requests
import pandas as pd
import os 
from utils.constants import FILE_PATH_TEMPLATE, TMP_PATH
from datetime import datetime
import logging
# Create and configure logger
logging.basicConfig(filename="data_analytics_challenge.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

log = logging.getLogger() #logging implement singleton.


class Extractor:
    
    def __init__(self, url, category: str) -> None:
        self.url = url
        self.category = category
        
    def extract(self) -> pd.DataFrame:
        log.info(f'Request for files from: {self.category}')
        #Get data from url.
        request = requests.get(self.url)
        request.encoding = 'utf-8'

        #Get current date.
        date = datetime.now()
        
        #Create path.
        relative_path = FILE_PATH_TEMPLATE.format(category=self.category,year=date.year,month=date.month,day=date.day)
        absolute_path = os.path.join(TMP_PATH,relative_path)
        dir_name = os.path.dirname(absolute_path)
        
        #Create directory if not exist.
        if not os.path.exists(dir_name):
            log.info(f'Creating path {dir_name}')
            os.makedirs(dir_name,exist_ok=True)
            
        #Write data to .csv  
        with open(absolute_path,'w') as f:
            log.info(f'Writing csv')
            f.write(request.text)
            
        return pd.read_csv(absolute_path)
    
    @abstractmethod
    def transform(self,df:pd.DataFrame) -> pd.DataFrame:
        pass
    

class MuseumExtractor(Extractor):
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        log.info(f'Transform {self.category} data.')
        cols_rename = {
            'Cod_Loc':'cod_localidad',
            'IdProvincia':'id_provincia',
            'IdDepartamento':'id_departamento',
            'categoria':'categoria',
            'provincia':'provincia',
            'localidad':'localidad',
            'nombre':'nombre',
            'direccion':'domicilio',
            'CP':'codigo_postal',
            'telefono':'numero_de_telefono',
            'Mail':'mail',
            'Web':'web'
        }
        df_museum_rename = pd.DataFrame()

        for k,v in cols_rename.items():
            df_museum_rename[v] = df[k]
        
        df_museum_rename['provincia'] = df_museum_rename['provincia'].apply(lambda x: str(x).replace(u'\xa0', u''))

        return df_museum_rename
    
    
class CinemaExtractor(Extractor):
     
     def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        log.info(f'Transform {self.category} data.')
        cols_rename = {
            'Cod_Loc':'cod_localidad',
            'IdProvincia':'id_provincia',
            'IdDepartamento':'id_departamento',
            'Categoría':'categoria',
            'Provincia':'provincia',
            'Localidad':'localidad',
            'Nombre':'nombre',
            'Dirección':'domicilio',
            'CP':'codigo_postal',
            'Teléfono':'numero_de_telefono',
            'Mail':'mail',
            'Web':'web'
        }
        df_cinema_rename = pd.DataFrame()

        for k,v in cols_rename.items():
            df_cinema_rename[v] = df[k]
        
        return df_cinema_rename
    
    
class LibraryExtractor(Extractor):
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        log.info(f'Transform {self.category} data.')
        cols_library = {
            'Cod_Loc':'cod_localidad',
            'IdProvincia':'id_provincia',
            'IdDepartamento':'id_departamento',
            'Categoría':'categoria',
            'Provincia':'provincia',
            'Localidad':'localidad',
            'Nombre':'nombre',
            'Domicilio':'domicilio',
            'CP':'codigo_postal',
            'Teléfono':'numero_de_telefono',
            'Mail':'mail',
            'Web':'web'
        }
        df_library_rename = pd.DataFrame()

        for k,v in cols_library.items():
            df_library_rename[v] = df[k]
        
        return df_library_rename