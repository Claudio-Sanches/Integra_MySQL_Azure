-- Views separadas para Power BI
-- Cada CREATE VIEW deve estar em seu próprio batch

USE [projeto-cbs];

-- Apagar views se existirem
DROP VIEW IF EXISTS vw_employee_summary;
DROP VIEW IF EXISTS vw_project_details;  
DROP VIEW IF EXISTS vw_executive_dashboard;

-- View 1: Employee Summary
CREATE VIEW vw_employee_summary AS
SELECT 
    e.Ssn,
    e.Fname + ' ' + ISNULL(e.Minit + ' ', '') + e.Lname as Full_Name,
    e.Fname, e.Lname, e.Sex, e.Bdate,
    DATEDIFF(YEAR, e.Bdate, GETDATE()) as Age,
    e.Address, e.Salary,
    d.Dname as Department_Name,
    d.Dnumber as Department_Number,
    CASE WHEN e.Super_ssn IS NULL THEN 'CEO' ELSE 'Employee' END as Position_Level
FROM employee e
LEFT JOIN departament d ON e.Dno = d.Dnumber;

-- View 2: Project Details
CREATE VIEW vw_project_details AS
SELECT 
    p.Pnumber, p.Pname as Project_Name, p.Plocation as Project_Location,
    d.Dname as Department_Name, d.Dnumber as Department_Number,
    COUNT(w.Essn) as Total_Employees,
    ISNULL(SUM(w.Hours), 0) as Total_Hours,
    ISNULL(AVG(w.Hours), 0) as Avg_Hours_Per_Employee
FROM project p
LEFT JOIN departament d ON p.Dnum = d.Dnumber
LEFT JOIN works_on w ON p.Pnumber = w.Pno
GROUP BY p.Pnumber, p.Pname, p.Plocation, d.Dname, d.Dnumber;

-- View 3: Executive Dashboard
CREATE VIEW vw_executive_dashboard AS
SELECT 
    (SELECT COUNT(*) FROM employee) as Total_Employees,
    (SELECT COUNT(*) FROM departament) as Total_Departments,
    (SELECT COUNT(*) FROM project) as Total_Projects,
    (SELECT SUM(Salary) FROM employee) as Total_Payroll,
    (SELECT AVG(Salary) FROM employee) as Average_Salary,
    (SELECT SUM(Hours) FROM works_on) as Total_Hours_Worked,
    (SELECT COUNT(*) FROM dependent) as Total_Dependents;