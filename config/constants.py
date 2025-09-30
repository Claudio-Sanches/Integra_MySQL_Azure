"""
Constantes do projeto
"""

# Ordem de remoção de tabelas (respeitando FKs)
TABLES_DROP_ORDER = [
    'works_on',
    'dependent', 
    'dept_locations',
    'project',
    'employee',
    'departament'
]

# Ordem de criação de tabelas
TABLES_CREATE_ORDER = [
    'departament',
    'employee',
    'project',
    'dept_locations',
    'works_on',
    'dependent'
]

# Views básicas
BASIC_VIEWS = [
    'vw_employee_summary',
    'vw_project_details'
]

# Views específicas para Power BI
POWERBI_VIEWS = [
    'vw_employee_manager',
    'vw_department_location', 
    'vw_employees_by_manager',
    'vw_powerbi_final'
]

# Mensagens de status
MESSAGES = {
    'connecting': "🔗 Conectando ao SQL Server...",
    'connected': "✅ Conectado com sucesso!",
    'cleanup': "🧹 LIMPEZA: Removendo tabelas existentes...",
    'creating': "🏗️ CRIAÇÃO: Criando estrutura das tabelas...",
    'relationships': "🔗 RELACIONAMENTOS: Adicionando Foreign Keys...",
    'data': "📊 DADOS: Inserindo registros...",
    'views': "📈 VIEWS: Criando views de consulta...",
    'powerbi_views': "📈 VIEWS POWER BI: Criando views para demandas específicas...",
    'verification': "🔍 VERIFICAÇÃO: Checando estrutura criada...",
    'success': "🎉 BANCO COMPANY CRIADO COM SUCESSO!",
    'closed': "🔌 Conexão fechada"
}