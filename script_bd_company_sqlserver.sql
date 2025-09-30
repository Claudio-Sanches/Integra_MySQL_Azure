-- Script para criar o banco de dados Company no SQL Server Azure
-- Compatível com SQL Server (não MySQL)

USE [projeto-cbs];

-- Verificar constraints existentes
SELECT 
    tc.CONSTRAINT_NAME,
    tc.TABLE_NAME,
    tc.CONSTRAINT_TYPE
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
WHERE TABLE_SCHEMA = 'dbo';

-- Criar tabela employee
CREATE TABLE employee(
    Fname VARCHAR(15) NOT NULL,
    Minit CHAR(1),
    Lname VARCHAR(15) NOT NULL,
    Ssn VARCHAR(9) NOT NULL, 
    Bdate DATE,
    Address VARCHAR(30),
    Sex CHAR(1),
    Salary NUMERIC(10,2),
    Super_ssn VARCHAR(9),
    Dno INT NOT NULL DEFAULT 1,
    CONSTRAINT chk_salary_employee CHECK (Salary > 2000.0),
    CONSTRAINT pk_employee PRIMARY KEY (Ssn)
);

-- Adicionar foreign key para supervisor (self-reference)
ALTER TABLE employee 
    ADD CONSTRAINT fk_employee_supervisor 
    FOREIGN KEY(Super_ssn) REFERENCES employee(Ssn);

-- Criar tabela departament
CREATE TABLE departament(
    Dname VARCHAR(15) NOT NULL,
    Dnumber INT NOT NULL,
    Mgr_ssn VARCHAR(9) NOT NULL,
    Mgr_start_date DATE, 
    Dept_create_date DATE,
    CONSTRAINT chk_date_dept CHECK (Dept_create_date < Mgr_start_date),
    CONSTRAINT pk_dept PRIMARY KEY (Dnumber),
    CONSTRAINT unique_name_dept UNIQUE(Dname),
    CONSTRAINT fk_dept_manager FOREIGN KEY (Mgr_ssn) REFERENCES employee(Ssn)
);

-- Adicionar foreign key de department para employee
ALTER TABLE employee 
    ADD CONSTRAINT fk_employee_dept 
    FOREIGN KEY(Dno) REFERENCES departament(Dnumber);

-- Criar tabela dept_locations
CREATE TABLE dept_locations(
    Dnumber INT NOT NULL,
    Dlocation VARCHAR(15) NOT NULL,
    CONSTRAINT pk_dept_locations PRIMARY KEY (Dnumber, Dlocation),
    CONSTRAINT fk_dept_locations FOREIGN KEY (Dnumber) REFERENCES departament(Dnumber)
        ON DELETE CASCADE
);

-- Criar tabela project
CREATE TABLE project(
    Pname VARCHAR(15) NOT NULL,
    Pnumber INT NOT NULL,
    Plocation VARCHAR(15),
    Dnum INT NOT NULL,
    CONSTRAINT pk_project PRIMARY KEY (Pnumber),
    CONSTRAINT unique_project UNIQUE (Pname),
    CONSTRAINT fk_project_dept FOREIGN KEY (Dnum) REFERENCES departament(Dnumber)
);

-- Criar tabela works_on
CREATE TABLE works_on(
    Essn VARCHAR(9) NOT NULL,
    Pno INT NOT NULL,
    Hours NUMERIC(3,1) NOT NULL,
    CONSTRAINT pk_works_on PRIMARY KEY (Essn, Pno),
    CONSTRAINT fk_employee_works_on FOREIGN KEY (Essn) REFERENCES employee(Ssn),
    CONSTRAINT fk_project_works_on FOREIGN KEY (Pno) REFERENCES project(Pnumber)
);

-- Criar tabela dependent
CREATE TABLE dependent(
    Essn VARCHAR(9) NOT NULL,
    Dependent_name VARCHAR(15) NOT NULL,
    Sex CHAR(1),
    Bdate DATE,
    Relationship VARCHAR(8),
    CONSTRAINT pk_dependent PRIMARY KEY (Essn, Dependent_name),
    CONSTRAINT fk_dependent_employee FOREIGN KEY (Essn) REFERENCES employee(Ssn)
);

-- Verificar tabelas criadas
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE' 
  AND TABLE_SCHEMA = 'dbo'
ORDER BY TABLE_NAME;

-- Verificar estrutura das tabelas
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'employee'
ORDER BY ORDINAL_POSITION;