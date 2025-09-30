"""
Criação da estrutura do banco (tabelas e relacionamentos)
"""
# IMPORTS CORRIGIDOS (sem ..)
from config.constants import TABLES_DROP_ORDER, MESSAGES
from utils.helpers import execute_command, print_section

class SchemaManager:
    """Gerencia a estrutura do banco de dados"""
    
    def __init__(self, cursor):
        self.cursor = cursor
    
    def cleanup_database(self):
        """Remove tabelas existentes na ordem correta"""
        print_section(MESSAGES['cleanup'])
        
        for table in TABLES_DROP_ORDER:
            execute_command(
                self.cursor, 
                f"DROP TABLE IF EXISTS {table}", 
                f"Remover {table}"
            )
    
    def create_tables(self):
        """Cria todas as tabelas na ordem correta"""
        print_section(MESSAGES['creating'])
        
        tables = {
            "Criar tabela departament": """
                CREATE TABLE departament(
                    Dnumber INT NOT NULL PRIMARY KEY,
                    Dname VARCHAR(15) NOT NULL UNIQUE,
                    Mgr_ssn VARCHAR(9),
                    Mgr_start_date DATE, 
                    Dept_create_date DATE
                )
            """,
            
            "Criar tabela employee": """
                CREATE TABLE employee(
                    Ssn VARCHAR(9) NOT NULL PRIMARY KEY,
                    Fname VARCHAR(15) NOT NULL,
                    Minit CHAR(1),
                    Lname VARCHAR(15) NOT NULL,
                    Bdate DATE,
                    Address VARCHAR(30),
                    Sex CHAR(1),
                    Salary NUMERIC(10,2),
                    Super_ssn VARCHAR(9),
                    Dno INT NOT NULL DEFAULT 1,
                    CONSTRAINT chk_salary_employee CHECK (Salary > 2000.0)
                )
            """,
            
            "Criar tabela project": """
                CREATE TABLE project(
                    Pnumber INT NOT NULL PRIMARY KEY,
                    Pname VARCHAR(15) NOT NULL UNIQUE,
                    Plocation VARCHAR(15),
                    Dnum INT NOT NULL
                )
            """,
            
            "Criar tabela dept_locations": """
                CREATE TABLE dept_locations(
                    Dnumber INT NOT NULL,
                    Dlocation VARCHAR(15) NOT NULL,
                    PRIMARY KEY (Dnumber, Dlocation)
                )
            """,
            
            "Criar tabela works_on": """
                CREATE TABLE works_on(
                    Essn VARCHAR(9) NOT NULL,
                    Pno INT NOT NULL,
                    Hours NUMERIC(3,1) NOT NULL,
                    PRIMARY KEY (Essn, Pno)
                )
            """,
            
            "Criar tabela dependent": """
                CREATE TABLE dependent(
                    Essn VARCHAR(9) NOT NULL,
                    Dependent_name VARCHAR(15) NOT NULL,
                    Sex CHAR(1),
                    Bdate DATE,
                    Relationship VARCHAR(8),
                    PRIMARY KEY (Essn, Dependent_name)
                )
            """
        }
        
        for description, sql in tables.items():
            execute_command(self.cursor, sql, description)
    
    def add_foreign_keys(self):
        """Adiciona as chaves estrangeiras após criação das tabelas"""
        print_section(MESSAGES['relationships'])
        
        foreign_keys = {
            "FK Employee → Departament": """
                ALTER TABLE employee 
                ADD CONSTRAINT fk_employee_dept 
                FOREIGN KEY (Dno) REFERENCES departament(Dnumber)
            """,
            
            "FK Employee → Supervisor": """
                ALTER TABLE employee 
                ADD CONSTRAINT fk_employee_super 
                FOREIGN KEY (Super_ssn) REFERENCES employee(Ssn)
            """,
            
            "FK Departament → Manager": """
                ALTER TABLE departament 
                ADD CONSTRAINT fk_dept_manager 
                FOREIGN KEY (Mgr_ssn) REFERENCES employee(Ssn)
            """,
            
            "FK Project → Departament": """
                ALTER TABLE project 
                ADD CONSTRAINT fk_project_dept 
                FOREIGN KEY (Dnum) REFERENCES departament(Dnumber)
            """,
            
            "FK Dept_locations → Departament": """
                ALTER TABLE dept_locations 
                ADD CONSTRAINT fk_deptloc_dept 
                FOREIGN KEY (Dnumber) REFERENCES departament(Dnumber)
            """,
            
            "FK Works_on → Employee": """
                ALTER TABLE works_on 
                ADD CONSTRAINT fk_workson_employee 
                FOREIGN KEY (Essn) REFERENCES employee(Ssn)
            """,
            
            "FK Works_on → Project": """
                ALTER TABLE works_on 
                ADD CONSTRAINT fk_workson_project 
                FOREIGN KEY (Pno) REFERENCES project(Pnumber)
            """,
            
            "FK Dependent → Employee": """
                ALTER TABLE dependent 
                ADD CONSTRAINT fk_dependent_employee 
                FOREIGN KEY (Essn) REFERENCES employee(Ssn)
            """
        }
        
        for description, sql in foreign_keys.items():
            execute_command(self.cursor, sql, description)
    
    def create_schema(self):
        """Executa criação completa do schema"""
        self.cleanup_database()
        self.create_tables()
        self.add_foreign_keys()