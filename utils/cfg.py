from decouple import RepositoryIni, Config


config = Config(RepositoryIni("settings.ini"))

#Database PostgreSQL
DB_CONNSTR = config("DB_CONNSTR")

#URLS
MUSEO_URL= config("MUSEO")
CINE_URL = config("CINE")
BIBLIOTECA_URL = config("BIBLIOTECA")