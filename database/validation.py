"""
Validação e verificação do banco de dados
"""
from config.constants import MESSAGES
from config.settings import DatabaseConfig
from utils.helpers import print_section, format_currency

class DatabaseValidator:
    """Classe para validar estrutura do banco"""
    
    def __init__(self, cursor):
        self.cursor = cursor
    
    def verify_database(self):
        """Verifica se o banco foi criado corretamente"""
        print_section(MESSAGES['verification'])
        
        # Verificar tabelas
        tables = self._get_tables()
        total_records = self._count_records(tables)
        
        # Verificar views
        views = self._get_views()
        
        # Teste de consulta
        self._test_query()
        
        # Resumo final
        self._print_summary(tables, views, total_records)
        
        return True
    
    def _get_tables(self):
        """Retorna lista de tabelas criadas"""
        self.cursor.execute("""
            SELECT name FROM sys.tables 
            WHERE type = 'U' AND name NOT LIKE 'sys%' 
            ORDER BY name
        """)
        return self.cursor.fetchall()
    
    def _get_views(self):
        """Retorna lista de views criadas"""
        self.cursor.execute("SELECT name FROM sys.views ORDER BY name")
        return self.cursor.fetchall()
    
    def _count_records(self, tables):
        """Conta registros em cada tabela"""
        print(f"\n📊 TABELAS CRIADAS ({len(tables)}):")
        total_records = 0
        
        for table in tables:
            table_name = table[0]
            self.cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
            count = self.cursor.fetchone()[0]
            total_records += count
            print(f"  📋 {table_name}: {count} registros")
        
        return total_records
    
    def _test_query(self):
        """Executa consulta de teste"""
        print(f"\n🎯 TESTE DE CONSULTA:")
        self.cursor.execute("""
            SELECT TOP 3 
                e.Fname + ' ' + e.Lname as Employee,
                d.Dname as Department,
                e.Salary
            FROM employee e
            JOIN departament d ON e.Dno = d.Dnumber
            ORDER BY e.Salary DESC
        """)
        
        employees = self.cursor.fetchall()
        print("  👥 Top 3 salários:")
        for emp in employees:
            print(f"    💰 {emp[0]} - {emp[1]} - {format_currency(emp[2])}")
    
    def _print_summary(self, tables, views, total_records):
        """Imprime resumo final"""
        print(f"\n{MESSAGES['success']}")
        print(f"✅ {len(tables)} tabelas, {len(views)} views, {total_records} registros")
        
        print(f"\n📋 INFORMAÇÕES PARA CONEXÃO:")
        print(f"🔗 Servidor: {DatabaseConfig.HOST}")
        print(f"🗃️ Database: {DatabaseConfig.DATABASE}")
        print(f"👤 Usuário: {DatabaseConfig.USER}")
        
        print(f"\n🎯 AGORA VOCÊ PODE:")
        print(f"  📊 Conectar no Power BI")
        print(f"  🔍 Executar consultas SQL")
        print(f"  📈 Usar as views criadas")
        
        print(f"\n📈 VIEWS PARA POWER BI:")
        print(f"  ✅ vw_employee_manager (Demandas 9,10,11)")
        print(f"  ✅ vw_department_location (Demanda 13)")
        print(f"  ✅ vw_employees_by_manager (Demanda 15)")
        print(f"  ✅ vw_powerbi_final (Demanda 16)")