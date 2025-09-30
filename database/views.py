"""
Criação de views para consultas e Power BI
"""
from config.constants import MESSAGES
from utils.helpers import execute_command, print_section

class ViewManager:
    """Gerencia criação de views"""
    
    def __init__(self, cursor):
        self.cursor = cursor
    
    def create_basic_views(self):
        """Cria views básicas para consultas"""
        print_section(MESSAGES['views'])
        
        basic_views = {
            "Criar view employee_summary": """
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
            """,
            
            "Criar view project_details": """
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
            """
        }
        
        for description, sql in basic_views.items():
            execute_command(self.cursor, sql, description)
    
    def create_powerbi_views(self):
        """Cria views específicas para Power BI (demandas 9-16)"""
        print_section(MESSAGES['powerbi_views'])
        
        powerbi_views = {
            "Criar view vw_employee_manager (Demandas 9,10,11)": """
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
            
            "Criar view vw_department_location (Demanda 13)": """
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
            
            "Criar view vw_employees_by_manager (Demanda 15)": """
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
            
            "Criar view vw_powerbi_final (Demanda 16)": """
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
        
        for description, sql in powerbi_views.items():
            execute_command(self.cursor, sql, description)
    
    def create_all_views(self):
        """Cria todas as views"""
        self.create_basic_views()
        self.create_powerbi_views()