# Challenge Data Analytics - Python 
> https://cdn.discordapp.com/attachments/670996715083399199/942821808619520091/Challenge_Data_Analytics_con_Python.pdf

- Objetive:

* 3 data sources.

    -> Cinema
    -> Museum
    -> Library

* Create SQL database.


# Prerequisites 


## Run DOCKER postgres.

Create container and volume.

    docker run -d --name data_challenge -v postgres_data:/var/lib/postgresql/data -p 5433:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=data_analitycs_challenge postgres

>-p localHost:dockerHost

Start if exited:

    docker start data_challenge

Execute command on container

    docker exec -it data_challenge psql -h localhost -U postgres -p 5432 -W -d data_analitycs_challenge

> -W, --password           force password prompt (should happen automatically)

> -d, --dbname=DBNAME      database name to connect to (default: "root")


# Usage

* Use this repo with a conda enviroment with all the requeriments packages:

        conda env create -f environment.yml
    
* To activate the environment:
    
        conda activate data_analitycs

* If you want to execute sql scripts use:

        python script_db.py
    
* To execute ETL pipeline:

        python main.py
    
    
* Update requeriments:

        conda list -e > environment.yml


