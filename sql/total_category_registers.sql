CREATE TABLE total_category_registers (
    job_date date NOT NULL,
    categoria varchar(255) NOT NULL,
    total int NOT NULL,
    CONSTRAINT PK_Total_Category_Registers PRIMARY KEY (job_date,categoria)
);
