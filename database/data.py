"""
Inserção de dados no banco
"""
# IMPORTS CORRIGIDOS (sem ..)
from config.constants import MESSAGES
from utils.helpers import execute_command, print_section

class DataManager:
    """Gerencia inserção de dados"""
    
    def __init__(self, cursor):
        self.cursor = cursor
    
    def insert_data(self):
        """Insere todos os dados na ordem correta"""
        print_section(MESSAGES['data'])
        
        # 1. Departamentos (sem managers)
        execute_command(self.cursor, """
            INSERT INTO departament (Dnumber, Dname, Mgr_ssn, Mgr_start_date, Dept_create_date) VALUES 
            (1, 'Headquarters', NULL, '1981-06-19', '1980-06-19'),
            (4, 'Administration', NULL, '1995-01-01', '1994-01-01'),
            (5, 'Research', NULL, '1988-05-22', '1986-05-22')
        """, "Inserir departamentos")
        
        # 2. Funcionários principais
        execute_command(self.cursor, """
            INSERT INTO employee VALUES 
            ('888665555', 'James', 'E', 'Borg', '1937-11-10', '450-Stone-Houston-TX', 'M', 55000, NULL, 1),
            ('333445555', 'Franklin', 'T', 'Wong', '1955-12-08', '638-Voss-Houston-TX', 'M', 40000, '888665555', 5),
            ('987654321', 'Jennifer', 'S', 'Wallace', '1941-06-20', '291-Berry-Bellaire-TX', 'F', 43000, '888665555', 4)
        """, "Inserir funcionários principais")
        
        # 3. Atualizar managers
        self._update_managers()
        
        # 4. Funcionários subordinados
        execute_command(self.cursor, """
            INSERT INTO employee VALUES 
            ('123456789', 'John', 'B', 'Smith', '1965-01-09', '731-Fondren-Houston-TX', 'M', 30000, '333445555', 5),
            ('666884444', 'Ramesh', 'K', 'Narayan', '1962-09-15', '975-Fire-Oak-Humble-TX', 'M', 38000, '333445555', 5),
            ('453453453', 'Joyce', 'A', 'English', '1972-07-31', '5631-Rice-Houston-TX', 'F', 25000, '333445555', 5),
            ('987987987', 'Ahmad', 'V', 'Jabbar', '1969-03-29', '980-Dallas-Houston-TX', 'M', 25000, '987654321', 4),
            ('999887777', 'Alicia', 'J', 'Zelaya', '1968-01-19', '3321-Castle-Spring-TX', 'F', 25000, '987654321', 4)
        """, "Inserir funcionários subordinados")
        
        # 5. Projetos
        execute_command(self.cursor, """
            INSERT INTO project VALUES 
            (1, 'ProductX', 'Bellaire', 5),
            (2, 'ProductY', 'Sugarland', 5),
            (3, 'ProductZ', 'Houston', 5),
            (10, 'Computerization', 'Stafford', 4),
            (20, 'Reorganization', 'Houston', 1),
            (30, 'Newbenefits', 'Stafford', 4)
        """, "Inserir projetos")
        
        # 6. Localizações
        execute_command(self.cursor, """
            INSERT INTO dept_locations VALUES 
            (1, 'Houston'),
            (4, 'Stafford'),
            (5, 'Bellaire'),
            (5, 'Sugarland'),
            (5, 'Houston')
        """, "Inserir localizações")
        
        # 7. Trabalho nos projetos
        execute_command(self.cursor, """
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
        execute_command(self.cursor, """
            INSERT INTO dependent VALUES 
            ('333445555', 'Alice', 'F', '1986-04-05', 'Daughter'),
            ('333445555', 'Theodore', 'M', '1983-10-25', 'Son'),
            ('333445555', 'Joy', 'F', '1958-05-03', 'Spouse'),
            ('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),
            ('123456789', 'Michael', 'M', '1988-01-04', 'Son'),
            ('123456789', 'Alice', 'F', '1988-12-30', 'Daughter'),
            ('123456789', 'Elizabeth', 'F', '1967-05-05', 'Spouse')
        """, "Inserir dependentes")
    
    def _update_managers(self):
        """Atualiza managers dos departamentos"""
        managers = {
            "Manager Headquarters": "UPDATE departament SET Mgr_ssn = '888665555' WHERE Dnumber = 1",
            "Manager Administration": "UPDATE departament SET Mgr_ssn = '987654321' WHERE Dnumber = 4", 
            "Manager Research": "UPDATE departament SET Mgr_ssn = '333445555' WHERE Dnumber = 5"
        }
        
        for description, sql in managers.items():
            execute_command(self.cursor, sql, description)