from cfg import DB_CONNSTR
from sqlalchemy import create_engine
from constants import TABLES, SQL_SRC
import logging
import os

# Create and configure logger
logging.basicConfig(filename="data_analytics_challenge.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')


engine = create_engine(DB_CONNSTR)
log = logging.getLogger() #logging implement singleton.

# Setting the threshold of logger.
log.setLevel(logging.INFO)

def create_tables():
    """Load and execute all the .sql scripts.
    """
    with engine.connect() as connection:
        for file in TABLES:
            log.info(f'Creating table from file {file}.sql')
            src = os.path.join(SQL_SRC,f'{file}.sql')
            print(src)
            with open(src,'r') as f:
                create_query = f.read()
            connection.execute(f'DROP TABLE IF EXISTS {file}')
            connection.execute(create_query)


if __name__ == '__main__':
    create_tables()