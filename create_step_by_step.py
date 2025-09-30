"""
Script para criar banco Company passo a passo - SQL Server Azure
Baseado nos arquivos insercao_de_dados_e_queries_sql.sql e script_bd_company.sql
"""
import pymssql
import os
from dotenv import load_dotenv

load_dotenv()

def execute_command(cursor, command, description):
    """Executa um comando SQL único"""
    try:
        cursor.execute(command)
        print(f"  ✅ {description}")
        return True
    except Exception as e:
        print(f"  ❌ {description}: {str(e)[:100]}...")
        return False

def cleanup_database(cursor):
    """Remove tabelas existentes na ordem correta"""
    print("🧹 LIMPEZA: Removendo tabelas existentes...")
    
    tables_to_drop = [
        'works_on',
        'dependent', 
        'dept_locations',
        'project',
        'employee',
        'departament'
    ]
    
    for table in tables_to_drop:
        execute_command(cursor, f"DROP TABLE IF EXISTS {table}", f"Remover {table}")

def create_tables(cursor):
    """Cria todas as tabelas na ordem correta"""
    print("\n🏗️ CRIAÇÃO: Criando estrutura das tabelas...")
    
    # 1. Departament (sem FK primeiro)
    execute_command(cursor, """
        CREATE TABLE departament(
            Dnumber INT NOT NULL PRIMARY KEY,
            Dname VARCHAR(15) NOT NULL UNIQUE,
            Mgr_ssn VARCHAR(9),
            Mgr_start_date DATE, 
            Dept_create_date DATE
        )
    """, "Criar tabela departament")
    
    # 2. Employee (sem FK de supervisor primeiro)
    execute_command(cursor, """
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
    """, "Criar tabela employee")
    
    # 3. Project
    execute_command(cursor, """
        CREATE TABLE project(
            Pnumber INT NOT NULL PRIMARY KEY,
            Pname VARCHAR(15) NOT NULL UNIQUE,
            Plocation VARCHAR(15),
            Dnum INT NOT NULL
        )
    """, "Criar tabela project")
    
    # 4. Dept_locations
    execute_command(cursor, """
        CREATE TABLE dept_locations(
            Dnumber INT NOT NULL,
            Dlocation VARCHAR(15) NOT NULL,
            PRIMARY KEY (Dnumber, Dlocation)
        )
    """, "Criar tabela dept_locations")
    
    # 5. Works_on
    execute_command(cursor, """
        CREATE TABLE works_on(
            Essn VARCHAR(9) NOT NULL,
            Pno INT NOT NULL,
            Hours NUMERIC(3,1) NOT NULL,
            PRIMARY KEY (Essn, Pno)
        )
    """, "Criar tabela works_on")
    
    # 6. Dependent
    execute_command(cursor, """
        CREATE TABLE dependent(
            Essn VARCHAR(9) NOT NULL,
            Dependent_name VARCHAR(15) NOT NULL,
            Sex CHAR(1),
            Bdate DATE,
            Relationship VARCHAR(8),
            PRIMARY KEY (Essn, Dependent_name)
        )
    """, "Criar tabela dependent")

def add_foreign_keys(cursor):
    """Adiciona as chaves estrangeiras após criação das tabelas"""
    print("\n🔗 RELACIONAMENTOS: Adicionando Foreign Keys...")
    
    # Employee -> Departament
    execute_command(cursor, """
        ALTER TABLE employee 
        ADD CONSTRAINT fk_employee_dept 
        FOREIGN KEY (Dno) REFERENCES departament(Dnumber)
    """, "FK Employee → Departament")
    
    # Employee -> Employee (supervisor)
    execute_command(cursor, """
        ALTER TABLE employee 
        ADD CONSTRAINT fk_employee_super 
        FOREIGN KEY (Super_ssn) REFERENCES employee(Ssn)
    """, "FK Employee → Supervisor")
    
    # Departament -> Employee (manager)
    execute_command(cursor, """
        ALTER TABLE departament 
        ADD CONSTRAINT fk_dept_manager 
        FOREIGN KEY (Mgr_ssn) REFERENCES employee(Ssn)
    """, "FK Departament → Manager")
    
    # Project -> Departament
    execute_command(cursor, """
        ALTER TABLE project 
        ADD CONSTRAINT fk_project_dept 
        FOREIGN KEY (Dnum) REFERENCES departament(Dnumber)
    """, "FK Project → Departament")
    
    # Dept_locations -> Departament
    execute_command(cursor, """
        ALTER TABLE dept_locations 
        ADD CONSTRAINT fk_deptloc_dept 
        FOREIGN KEY (Dnumber) REFERENCES departament(Dnumber)
    """, "FK Dept_locations → Departament")
    
    # Works_on -> Employee
    execute_command(cursor, """
        ALTER TABLE works_on 
        ADD CONSTRAINT fk_workson_employee 
        FOREIGN KEY (Essn) REFERENCES employee(Ssn)
    """, "FK Works_on → Employee")
    
    # Works_on -> Project
    execute_command(cursor, """
        ALTER TABLE works_on 
        ADD CONSTRAINT fk_workson_project 
        FOREIGN KEY (Pno) REFERENCES project(Pnumber)
    """, "FK Works_on → Project")
    
    # Dependent -> Employee
    execute_command(cursor, """
        ALTER TABLE dependent 
        ADD CONSTRAINT fk_dependent_employee 
        FOREIGN KEY (Essn) REFERENCES employee(Ssn)
    """, "FK Dependent → Employee")

def insert_data(cursor):
    """Insere todos os dados na ordem correta"""
    print("\n📊 DADOS: Inserindo registros...")
    
    # 1. Departamentos (sem managers primeiro)
    execute_command(cursor, """
        INSERT INTO departament (Dnumber, Dname, Mgr_ssn, Mgr_start_date, Dept_create_date) VALUES 
        (1, 'Headquarters', NULL, '1981-06-19', '1980-06-19'),
        (4, 'Administration', NULL, '1995-01-01', '1994-01-01'),
        (5, 'Research', NULL, '1988-05-22', '1986-05-22')
    """, "Inserir departamentos")
    
    # 2. Funcionários principais (CEOs/Managers)
    execute_command(cursor, """
        INSERT INTO employee VALUES 
        ('888665555', 'James', 'E', 'Borg', '1937-11-10', '450-Stone-Houston-TX', 'M', 55000, NULL, 1),
        ('333445555', 'Franklin', 'T', 'Wong', '1955-12-08', '638-Voss-Houston-TX', 'M', 40000, '888665555', 5),
        ('987654321', 'Jennifer', 'S', 'Wallace', '1941-06-20', '291-Berry-Bellaire-TX', 'F', 43000, '888665555', 4)
    """, "Inserir funcionários principais")
    
    # 3. Atualizar managers dos departamentos
    execute_command(cursor, "UPDATE departament SET Mgr_ssn = '888665555' WHERE Dnumber = 1", "Manager Headquarters")
    execute_command(cursor, "UPDATE departament SET Mgr_ssn = '987654321' WHERE Dnumber = 4", "Manager Administration")
    execute_command(cursor, "UPDATE departament SET Mgr_ssn = '333445555' WHERE Dnumber = 5", "Manager Research")
    
    # 4. Funcionários subordinados
    execute_command(cursor, """
        INSERT INTO employee VALUES 
        ('123456789', 'John', 'B', 'Smith', '1965-01-09', '731-Fondren-Houston-TX', 'M', 30000, '333445555', 5),
        ('666884444', 'Ramesh', 'K', 'Narayan', '1962-09-15', '975-Fire-Oak-Humble-TX', 'M', 38000, '333445555', 5),
        ('453453453', 'Joyce', 'A', 'English', '1972-07-31', '5631-Rice-Houston-TX', 'F', 25000, '333445555', 5),
        ('987987987', 'Ahmad', 'V', 'Jabbar', '1969-03-29', '980-Dallas-Houston-TX', 'M', 25000, '987654321', 4),
        ('999887777', 'Alicia', 'J', 'Zelaya', '1968-01-19', '3321-Castle-Spring-TX', 'F', 25000, '987654321', 4)
    """, "Inserir funcionários subordinados")
    
    # 5. Projetos
    execute_command(cursor, """
        INSERT INTO project VALUES 
        (1, 'ProductX', 'Bellaire', 5),
        (2, 'ProductY', 'Sugarland', 5),
        (3, 'ProductZ', 'Houston', 5),
        (10, 'Computerization', 'Stafford', 4),
        (20, 'Reorganization', 'Houston', 1),
        (30, 'Newbenefits', 'Stafford', 4)
    """, "Inserir projetos")
    
    # 6. Localizações dos departamentos
    execute_command(cursor, """
        INSERT INTO dept_locations VALUES 
        (1, 'Houston'),
        (4, 'Stafford'),
        (5, 'Bellaire'),
        (5, 'Sugarland'),
        (5, 'Houston')
    """, "Inserir localizações")
    
    # 7. Trabalho nos projetos
    execute_command(cursor, """
        INSERT INTO works_on VALUES 
        ('123456789', 1, 32.5),
        ('123456789', 2, 7.5),
        ('666884444', 3, 40.0),
        ('453453453', 1, 20.0),
        ('453453453', 2, 20.0),
        ('333445555', 2, 10.0),
        ('333445555', 3, 10.0),
        ('333445555', 10, 10.0),
        ('333445555', 20, 10.0),
        ('999887777', 30, 30.0),
        ('999887777', 10, 10.0),
        ('987987987', 10, 35.0),
        ('987987987', 30, 5.0),
        ('987654321', 30, 20.0),
        ('987654321', 20, 15.0),
        ('888665555', 20, 0.0)
    """, "Inserir trabalhos nos projetos")
    
    # 8. Dependentes
    execute_command(cursor, """
        INSERT INTO dependent VALUES 
        ('333445555', 'Alice', 'F', '1986-04-05', 'Daughter'),
        ('333445555', 'Theodore', 'M', '1983-10-25', 'Son'),
        ('333445555', 'Joy', 'F', '1958-05-03', 'Spouse'),
        ('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),
        ('123456789', 'Michael', 'M', '1988-01-04', 'Son'),
        ('123456789', 'Alice', 'F', '1988-12-30', 'Daughter'),
        ('123456789', 'Elizabeth', 'F', '1967-05-05', 'Spouse')
    """, "Inserir dependentes")

def create_views(cursor):
    """Cria views úteis para consultas"""
    print("\n📈 VIEWS: Criando views de consulta...")
    
    execute_command(cursor, """
        CREATE VIEW vw_employee_summary AS
        SELECT 
            e.Ssn,
            e.Fname + ' ' + ISNULL(e.Minit + ' ', '') + e.Lname as Full_Name,
            e.Fname, e.Lname, e.Sex, e.Bdate,
            DATEDIFF(YEAR, e.Bdate, GETDATE()) as Age,
            e.Address, e.Salary,
            d.Dname as Department_Name,
            CASE WHEN e.Super_ssn IS NULL THEN 'CEO' ELSE 'Employee' END as Position_Level
        FROM employee e
        LEFT JOIN departament d ON e.Dno = d.Dnumber
    """, "Criar view employee_summary")
    
    execute_command(cursor, """
        CREATE VIEW vw_project_details AS
        SELECT 
            p.Pnumber, p.Pname as Project_Name, p.Plocation,
            d.Dname as Department_Name,
            COUNT(w.Essn) as Total_Employees,
            ISNULL(SUM(w.Hours), 0) as Total_Hours
        FROM project p
        LEFT JOIN departament d ON p.Dnum = d.Dnumber
        LEFT JOIN works_on w ON p.Pnumber = w.Pno
        GROUP BY p.Pnumber, p.Pname, p.Plocation, d.Dname
    """, "Criar view project_details")

def create_powerbi_demand_views(cursor):
    """Cria views específicas para atender demandas Power BI"""
    
    views = {
        "vw_employee_manager": """
        CREATE VIEW vw_employee_manager AS
        SELECT 
            e.Ssn as Employee_SSN,
            e.Fname + ' ' + ISNULL(e.Minit + ' ', '') + e.Lname as Employee_Full_Name,
            e.Sex as Employee_Gender,
            e.Salary as Employee_Salary,
            DATEDIFF(YEAR, e.Bdate, GETDATE()) as Employee_Age,
            d.Dname as Department_Name,
            mgr.Fname + ' ' + ISNULL(mgr.Minit + ' ', '') + mgr.Lname as Manager_Full_Name,
            mgr.Ssn as Manager_SSN,
            CASE 
                WHEN e.Super_ssn IS NULL THEN 'CEO'
                ELSE 'Employee' 
            END as Employee_Level
        FROM employee e
        LEFT JOIN departament d ON e.Dno = d.Dnumber
        LEFT JOIN employee mgr ON d.Mgr_ssn = mgr.Ssn
        """,
        
        "vw_department_location": """
        CREATE VIEW vw_department_location AS
        SELECT 
            d.Dnumber as Department_Number,
            d.Dname as Department_Name,
            dl.Dlocation as Department_Location,
            d.Dname + ' - ' + dl.Dlocation as Department_Location_Combined,
            mgr.Fname + ' ' + ISNULL(mgr.Minit + ' ', '') + mgr.Lname as Manager_Full_Name
        FROM departament d
        INNER JOIN dept_locations dl ON d.Dnumber = dl.Dnumber
        LEFT JOIN employee mgr ON d.Mgr_ssn = mgr.Ssn
        """,
        
        "vw_employees_by_manager": """
        CREATE VIEW vw_employees_by_manager AS
        SELECT 
            mgr.Ssn as Manager_SSN,
            mgr.Fname + ' ' + ISNULL(mgr.Minit + ' ', '') + mgr.Lname as Manager_Full_Name,
            d.Dname as Department_Name,
            COUNT(e.Ssn) as Total_Employees,
            AVG(e.Salary) as Average_Team_Salary,
            SUM(e.Salary) as Total_Team_Payroll
        FROM employee mgr
        INNER JOIN departament d ON mgr.Ssn = d.Mgr_ssn
        LEFT JOIN employee e ON d.Dnumber = e.Dno
        GROUP BY mgr.Ssn, mgr.Fname, mgr.Minit, mgr.Lname, d.Dname
        """,
        
        "vw_powerbi_final": """
        CREATE VIEW vw_powerbi_final AS
        SELECT 
            e.Ssn as Employee_ID,
            d.Dnumber as Department_ID,
            e.Fname + ' ' + ISNULL(e.Minit + ' ', '') + e.Lname as Employee_Name,
            mgr.Fname + ' ' + ISNULL(mgr.Minit + ' ', '') + mgr.Lname as Manager_Name,
            d.Dname + ' - ' + COALESCE(
                (SELECT TOP 1 dl.Dlocation 
                 FROM dept_locations dl 
                 WHERE dl.Dnumber = d.Dnumber), 
                'No Location'
            ) as Department_Location,
            e.Salary as Salary,
            DATEDIFF(YEAR, e.Bdate, GETDATE()) as Age,
            e.Sex as Gender,
            CASE 
                WHEN e.Super_ssn IS NULL THEN 'CEO'
                WHEN e.Ssn IN (SELECT Mgr_ssn FROM departament) THEN 'Manager'
                ELSE 'Employee' 
            END as Position_Level,
            CASE 
                WHEN e.Salary >= 50000 THEN 'High'
                WHEN e.Salary >= 35000 THEN 'Medium'
                ELSE 'Low' 
            END as Salary_Range
        FROM employee e
        LEFT JOIN departament d ON e.Dno = d.Dnumber
        LEFT JOIN employee mgr ON d.Mgr_ssn = mgr.Ssn
        """
    }
    
    print("\n📈 VIEWS POWER BI: Criando views para demandas específicas...")
    
    for view_name, view_sql in views.items():
        execute_command(cursor, view_sql, f"Criar view {view_name}")

def verify_database(cursor):
    """Verifica se o banco foi criado corretamente"""
    print("\n🔍 VERIFICAÇÃO: Checando estrutura criada...")
    
    # Verificar tabelas
    cursor.execute("""
        SELECT name FROM sys.tables 
        WHERE type = 'U' AND name NOT LIKE 'sys%' 
        ORDER BY name
    """)
    tables = cursor.fetchall()
    
    print(f"\n📊 TABELAS CRIADAS ({len(tables)}):")
    total_records = 0
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
        count = cursor.fetchone()[0]
        total_records += count
        print(f"  📋 {table_name}: {count} registros")
    
    # Verificar views
    cursor.execute("SELECT name FROM sys.views ORDER BY name")
    views = cursor.fetchall()
    print(f"\n📈 VIEWS CRIADAS ({len(views)}):")
    for view in views:
        print(f"  📊 {view[0]}")
    
    # Teste de consulta
    print(f"\n🎯 TESTE DE CONSULTA:")
    cursor.execute("""
        SELECT TOP 3 
            e.Fname + ' ' + e.Lname as Employee,
            d.Dname as Department,
            e.Salary
        FROM employee e
        JOIN departament d ON e.Dno = d.Dnumber
        ORDER BY e.Salary DESC
    """)
    
    employees = cursor.fetchall()
    print("  👥 Top 3 salários:")
    for emp in employees:
        print(f"    💰 {emp[0]} - {emp[1]} - ${emp[2]:,.2f}")
    
    print(f"\n🎉 BANCO COMPANY CRIADO COM SUCESSO!")
    print(f"✅ {len(tables)} tabelas, {len(views)} views, {total_records} registros")
    return True

def main():
    """Função principal"""
    try:
        print("🚀 CRIANDO BANCO COMPANY - SQL SERVER AZURE")
        print("=" * 50)
        
        # Conectar
        print("🔗 Conectando ao SQL Server...")
        connection = pymssql.connect(
            server=os.getenv('MYSQL_HOST'),
            database=os.getenv('MYSQL_DATABASE'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            port=int(os.getenv('MYSQL_PORT', 1433)),
            autocommit=True
        )
        
        cursor = connection.cursor()
        print("✅ Conectado com sucesso!")
        
        # Executar passos
        cleanup_database(cursor)
        create_tables(cursor)
        add_foreign_keys(cursor)
        insert_data(cursor)
        create_views(cursor)
        create_powerbi_demand_views(cursor)
        
        # Verificação final
        success = verify_database(cursor)
        
        if success:
            print(f"\n📋 INFORMAÇÕES PARA CONEXÃO:")
            print(f"🔗 Servidor: {os.getenv('MYSQL_HOST')}")
            print(f"🗃️ Database: {os.getenv('MYSQL_DATABASE')}")
            print(f"👤 Usuário: {os.getenv('MYSQL_USER')}")
            print(f"\n🎯 AGORA VOCÊ PODE:")
            print(f"  📊 Conectar no Power BI")
            print(f"  🔍 Executar consultas SQL")
            print(f"  📈 Usar as views criadas")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        
    finally:
        if 'connection' in locals():
            connection.close()
            print("🔌 Conexão fechada")

if __name__ == "__main__":
    main()