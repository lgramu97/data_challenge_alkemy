CREATE TABLE total_category_prov_registers (
    source varchar(255) NOT NULL,
    province varchar(255) NOT NULL,
    total int NOT NULL,
    CONSTRAINT PK_Registers PRIMARY KEY (source,province)
);