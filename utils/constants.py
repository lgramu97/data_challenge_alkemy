import os
from pathlib import Path
#SQL src
ROOT = Path().resolve().parent
SQL_SRC = os.path.join(ROOT,'data_challenge_alkemy/sql')

#Table IDs
MAIN_TABLE = 'raw'
CATEGORY_REGISTER = 'total_category_registers'
SOURCE_REGISTER = 'total_source_registers'
CATEGORY_PROV_REGISTER = 'total_category_prov_registers'
CINE_TABLE = 'cine_table'

TABLES = [MAIN_TABLE, CATEGORY_REGISTER,
          SOURCE_REGISTER, CATEGORY_PROV_REGISTER,
          CINE_TABLE]

FILE_PATH_TEMPLATE = '{category}/{year}-{month:02d}/{category}-{year}-{month:02d}-{day:02d}.csv'
TMP_PATH = os.path.join(Path().resolve().parent,'data_challenge_alkemy/files')
