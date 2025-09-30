"""
Script principal - Criação do banco Company
Versão modular seguindo melhores práticas
"""
# IMPORTS CORRIGIDOS (sem src.)
from config.settings import AppConfig, DatabaseConfig
from database.connection import DatabaseConnection
from database.schema import SchemaManager
from database.data import DataManager
from database.views import ViewManager
from database.validation import DatabaseValidator
from utils.helpers import print_header

def main():
    """Função principal do sistema"""
    try:
        # Cabeçalho
        print_header(f"🚀 {AppConfig.PROJECT_NAME}")
        print(f"📋 {AppConfig.DESCRIPTION}")
        print(f"🔧 Versão: {AppConfig.VERSION}")
        
        # Usar context manager para conexão
        with DatabaseConnection() as db:
            cursor = db.get_cursor()
            
            # Instanciar managers
            schema_manager = SchemaManager(cursor)
            data_manager = DataManager(cursor)
            view_manager = ViewManager(cursor)
            validator = DatabaseValidator(cursor)
            
            # Executar pipeline completo
            schema_manager.create_schema()
            data_manager.insert_data()
            view_manager.create_all_views()
            validator.verify_database()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)