import os

#SQL src
ROOT = os.path.dirname(os.path.abspath(__file__))
SQL_SRC = os.path.join(ROOT,'sql')

#Table IDs
MAIN_TABLE = 'raw'
CATEGORY_REGISTER = 'total_category_registers'
SOURCE_REGISTER = 'total_source_registers'
CATEGORY_PROV_REGISTER = 'total_category_prov_registers'
CINE_TABLE = 'cine_table'

TABLES = [MAIN_TABLE, CATEGORY_REGISTER,
          SOURCE_REGISTER, CATEGORY_PROV_REGISTER,
          CINE_TABLE]