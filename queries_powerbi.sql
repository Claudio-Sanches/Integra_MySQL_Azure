-- Queries SQL otimizadas para Power BI
-- Use estas queries no Power BI para importar dados

-- 1. FUNCIONÁRIOS (Tabela principal)
SELECT 
    e.Ssn as Employee_ID,
    e.Fname + ' ' + ISNULL(e.Minit + ' ', '') + e.Lname as Full_Name,
    e.Fname as First_Name,
    e.Lname as Last_Name,
    e.Sex as Gender,
    e.Bdate as Birth_Date,
    DATEDIFF(YEAR, e.Bdate, GETDATE()) as Age,
    CASE 
        WHEN DATEDIFF(YEAR, e.Bdate, GETDATE()) < 30 THEN 'Jovem'
        WHEN DATEDIFF(YEAR, e.Bdate, GETDATE()) < 50 THEN 'Adulto'
        ELSE 'Experiente'
    END as Age_Group,
    e.Address,
    e.Salary,
    CASE 
        WHEN e.Salary < 30000 THEN 'Baixo'
        WHEN e.Salary < 45000 THEN 'Médio'
        ELSE 'Alto'
    END as Salary_Range,
    e.Dno as Department_Number,
    e.Super_ssn as Supervisor_ID,
    CASE WHEN e.Super_ssn IS NULL THEN 'CEO' ELSE 'Funcionário' END as Position_Level
FROM employee e;

-- 2. DEPARTAMENTOS
SELECT 
    d.Dnumber as Department_Number,
    d.Dname as Department_Name,
    d.Mgr_ssn as Manager_ID,
    d.Mgr_start_date as Manager_Start_Date,
    d.Dept_create_date as Department_Create_Date,
    DATEDIFF(YEAR, d.Dept_create_date, GETDATE()) as Department_Age_Years
FROM departament d;

-- 3. PROJETOS
SELECT 
    p.Pnumber as Project_Number,
    p.Pname as Project_Name,
    p.Plocation as Project_Location,
    p.Dnum as Department_Number
FROM project p;

-- 4. HORAS TRABALHADAS (Para análise de produtividade)
SELECT 
    w.Essn as Employee_ID,
    w.Pno as Project_Number,
    w.Hours as Hours_Worked,
    CASE 
        WHEN w.Hours = 0 THEN 'Não Trabalhado'
        WHEN w.Hours < 10 THEN 'Baixa'
        WHEN w.Hours < 30 THEN 'Média'
        ELSE 'Alta'
    END as Work_Intensity
FROM works_on w;

-- 5. LOCALIZAÇÕES DOS DEPARTAMENTOS
SELECT 
    dl.Dnumber as Department_Number,
    dl.Dlocation as Location
FROM dept_locations dl;

-- 6. DEPENDENTES (Para análise de benefícios)
SELECT 
    dep.Essn as Employee_ID,
    dep.Dependent_name as Dependent_Name,
    dep.Sex as Dependent_Gender,
    dep.Bdate as Dependent_Birth_Date,
    DATEDIFF(YEAR, dep.Bdate, GETDATE()) as Dependent_Age,
    dep.Relationship
FROM dependent dep;

-- 7. RESUMO EXECUTIVO (Para KPIs)
SELECT 
    'Total Funcionários' as Metric,
    COUNT(*) as Value,
    'pessoas' as Unit
FROM employee
UNION ALL
SELECT 
    'Folha de Pagamento Total',
    SUM(Salary),
    'reais'
FROM employee
UNION ALL
SELECT 
    'Salário Médio',
    AVG(Salary),
    'reais'
FROM employee
UNION ALL
SELECT 
    'Total Projetos',
    COUNT(*),
    'projetos'
FROM project
UNION ALL
SELECT 
    'Total Horas Trabalhadas',
    SUM(Hours),
    'horas'
FROM works_on
UNION ALL
SELECT 
    'Total Dependentes',
    COUNT(*),
    'pessoas'
FROM dependent;

-- 8. ANÁLISE DE PRODUTIVIDADE POR FUNCIONÁRIO
SELECT 
    e.Ssn as Employee_ID,
    e.Fname + ' ' + e.Lname as Employee_Name,
    d.Dname as Department,
    COUNT(DISTINCT w.Pno) as Projects_Count,
    SUM(w.Hours) as Total_Hours,
    AVG(w.Hours) as Avg_Hours_Per_Project,
    e.Salary,
    CASE 
        WHEN SUM(w.Hours) IS NULL THEN 0
        ELSE ROUND(e.Salary / NULLIF(SUM(w.Hours), 0), 2)
    END as Cost_Per_Hour
FROM employee e
LEFT JOIN departament d ON e.Dno = d.Dnumber
LEFT JOIN works_on w ON e.Ssn = w.Essn
GROUP BY e.Ssn, e.Fname, e.Lname, d.Dname, e.Salary;

-- 9. ANÁLISE DE PROJETOS
SELECT 
    p.Pnumber as Project_Number,
    p.Pname as Project_Name,
    p.Plocation as Location,
    d.Dname as Department,
    COUNT(w.Essn) as Employees_Assigned,
    SUM(w.Hours) as Total_Hours,
    SUM(e.Salary * w.Hours / 2080) as Estimated_Cost -- Assumindo 2080 horas/ano
FROM project p
LEFT JOIN departament d ON p.Dnum = d.Dnumber
LEFT JOIN works_on w ON p.Pnumber = w.Pno
LEFT JOIN employee e ON w.Essn = e.Ssn
GROUP BY p.Pnumber, p.Pname, p.Plocation, d.Dname;

-- 10. HIERARQUIA ORGANIZACIONAL
SELECT 
    e.Ssn as Employee_ID,
    e.Fname + ' ' + e.Lname as Employee_Name,
    e.Super_ssn as Supervisor_ID,
    sup.Fname + ' ' + sup.Lname as Supervisor_Name,
    d.Dname as Department
FROM employee e
LEFT JOIN employee sup ON e.Super_ssn = sup.Ssn
LEFT JOIN departament d ON e.Dno = d.Dnumber;