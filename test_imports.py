"""
Teste apenas dos imports
"""

def test_imports():
    print("🧪 TESTE DE IMPORTS")
    print("=" * 25)
    
    try:
        print("📋 Testando config...")
        from config.settings import AppConfig, DatabaseConfig
        from config.constants import MESSAGES
        print("  ✅ Config OK")
        
        print("🛠️ Testando utils...")
        from utils.helpers import execute_command, print_header
        print("  ✅ Utils OK")
        
        print("🔗 Testando database...")
        try:
            from database.connection import DatabaseConnection
            print("  ✅ Database Connection OK")
        except ImportError as e:
            if "pymssql" in str(e):
                print("  ⚠️ Database Connection: pymssql não instalado")
            else:
                raise e
        
        from database.schema import SchemaManager
        print("  ✅ Database Schema OK")
        
        print(f"\n🎉 ESTRUTURA FUNCIONANDO!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Outro erro: {e}")
        return False

if __name__ == "__main__":
    test_imports()