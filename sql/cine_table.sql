CREATE TABLE cine_table(
    provincia varchar(255) NOT NULL,
    job_date date NOT NULL, 
    cantidad_pantallas int NOT NULL,
    cantidad_butacas int NOT NULL,
    cantidad_incaa int NOT NULL,
    CONSTRAINT PK_Cine PRIMARY KEY (job_date,provincia)
);

--Job_Date is the day when the process run. Its PK because u can track history.