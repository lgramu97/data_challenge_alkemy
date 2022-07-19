CREATE TABLE total_category_prov_registers (
    job_date date NOT NULL, 
    categoria varchar(255) NOT NULL,
    provincia varchar(255) NOT NULL,
    total int NOT NULL,
    CONSTRAINT PK_Registers PRIMARY KEY (job_date,categoria,provincia)
);

