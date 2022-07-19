CREATE TABLE total_source_registers (
    job_date date NOT NULL, 
    source varchar(255) NOT NULL,
    total int NOT NULL,
    CONSTRAINT PK_Total_Source_Registers PRIMARY KEY (job_date,source)
);  
