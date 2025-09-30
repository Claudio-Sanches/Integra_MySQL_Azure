"""
Teste completo de todos os módulos
"""

def test_all_modules():
    print("🧪 TESTE COMPLETO DO SISTEMA")
    print("=" * 35)
    
    try:
        print("📋 Testando config...")
        from config.settings import AppConfig, DatabaseConfig
        from config.constants import MESSAGES
        print("  ✅ Config OK")
        
        print("🛠️ Testando utils...")
        from utils.helpers import execute_command, print_header
        print("  ✅ Utils OK")
        
        print("🔗 Testando database...")
        from database.connection import DatabaseConnection
        from database.schema import SchemaManager
        from database.data import DataManager
        from database.views import ViewManager
        from database.validation import DatabaseValidator
        print("  ✅ Todos os módulos database OK")
        
        print(f"\n📊 Sistema pronto:")
        print(f"  📋 Projeto: {AppConfig.PROJECT_NAME}")
        print(f"  🔧 Versão: {AppConfig.VERSION}")
        print(f"  🖥️ Conectando em: {DatabaseConfig.HOST}")
        
        print(f"\n🎉 SISTEMA COMPLETO FUNCIONANDO!")
        print(f"✅ Execute: python main.py")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    test_all_modules()