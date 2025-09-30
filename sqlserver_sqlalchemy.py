import urllib.parse
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config import MySQLConfig

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLServerConnectionSQLAlchemy:
    """Classe para gerenciar conexões com SQL Server usando SQLAlchemy"""
    
    def __init__(self):
        self.engine = None
        self.connection = None
    
    def create_engine(self):
        """Cria engine SQLAlchemy para SQL Server"""
        try:
            # Validar configurações
            MySQLConfig.validate_config()
            params = MySQLConfig.get_connection_params()
            
            # Construir connection string
            connection_string = (
                f"mssql+pymssql://{urllib.parse.quote_plus(params['user'])}:"
                f"{urllib.parse.quote_plus(params['password'])}@"
                f"{params['host']}:{params['port']}/"
                f"{params['database']}?"
                f"charset=utf8"
            )
            
            logger.info(f"Criando engine para: {params['host']}")
            logger.info(f"Banco de dados: {params['database']}")
            
            # Criar engine
            self.engine = create_engine(
                connection_string,
                echo=False,  # Set to True for SQL debugging
                pool_timeout=30,
                pool_recycle=3600
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar engine: {e}")
            return False
    
    def connect(self):
        """Estabelece conexão com o banco"""
        try:
            if not self.engine and not self.create_engine():
                return False
            
            # Testar conexão
            self.connection = self.engine.connect()
            
            # Teste simples
            result = self.connection.execute(text("SELECT 1 as test"))
            test_result = result.fetchone()
            
            if test_result and test_result[0] == 1:
                logger.info("✅ Conexão SQLAlchemy estabelecida com sucesso!")
                return True
            else:
                logger.error("❌ Falha no teste de conexão")
                return False
                
        except SQLAlchemyError as e:
            logger.error(f"❌ Erro SQLAlchemy: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}")
            return False
    
    def disconnect(self):
        """Fecha conexão"""
        try:
            if self.connection:
                self.connection.close()
            if self.engine:
                self.engine.dispose()
            logger.info("Conexão fechada")
        except Exception as e:
            logger.error(f"Erro ao fechar conexão: {e}")
    
    def execute_query(self, query, params=None):
        """Executa query SELECT"""
        try:
            if not self.connection:
                logger.error("Sem conexão ativa")
                return None
            
            if params:
                result = self.connection.execute(text(query), params)
            else:
                result = self.connection.execute(text(query))
            
            return result.fetchall()
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao executar query: {e}")
            return None
    
    def execute_non_query(self, query, params=None):
        """Executa INSERT, UPDATE, DELETE"""
        try:
            if not self.connection:
                logger.error("Sem conexão ativa")
                return False
            
            if params:
                result = self.connection.execute(text(query), params)
            else:
                result = self.connection.execute(text(query))
            
            self.connection.commit()
            logger.info(f"Query executada. Linhas afetadas: {result.rowcount}")
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao executar query: {e}")
            self.connection.rollback()
            return False
    
    def get_tables(self):
        """Lista tabelas do banco"""
        query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """
        results = self.execute_query(query)
        if results:
            return [row[0] for row in results]
        return []
    
    def test_connection(self):
        """Teste completo de conexão"""
        logger.info("=== Iniciando Teste SQLAlchemy ===")
        
        if self.connect():
            try:
                # Teste básico
                logger.info("✅ Conexão estabelecida")
                
                # Informações do servidor
                version_query = "SELECT @@VERSION"
                version_result = self.execute_query(version_query)
                if version_result:
                    version_info = version_result[0][0]
                    logger.info(f"SQL Server: {version_info.split()[3]}")
                
                # Informações do banco
                db_query = "SELECT DB_NAME() as database_name"
                db_result = self.execute_query(db_query)
                if db_result:
                    logger.info(f"Banco ativo: {db_result[0][0]}")
                
                # Listar tabelas
                tables = self.get_tables()
                if tables:
                    logger.info(f"Tabelas encontradas ({len(tables)}): {tables}")
                else:
                    logger.info("Nenhuma tabela encontrada")
                
                # Teste de privilégios
                try:
                    privs_query = """
                    SELECT 
                        HAS_PERMS_BY_NAME(null, null, 'CONTROL SERVER') as control_server,
                        HAS_PERMS_BY_NAME(DB_NAME(), 'DATABASE', 'SELECT') as db_select,
                        HAS_PERMS_BY_NAME(DB_NAME(), 'DATABASE', 'INSERT') as db_insert
                    """
                    privs_result = self.execute_query(privs_query)
                    if privs_result:
                        row = privs_result[0]
                        logger.info(f"Privilégios - SELECT: {bool(row[1])}, INSERT: {bool(row[2])}")
                except:
                    logger.info("Não foi possível verificar privilégios")
                
                self.disconnect()
                return True
                
            except Exception as e:
                logger.error(f"Erro durante teste: {e}")
                self.disconnect()
                return False
        else:
            return False

def test_sqlalchemy_connection():
    """Teste rápido SQLAlchemy"""
    db = SQLServerConnectionSQLAlchemy()
    return db.test_connection()

if __name__ == "__main__":
    print("=== Teste SQLAlchemy SQL Server Azure ===")
    success = test_sqlalchemy_connection()
    
    if success:
        print("\n✅ SUCESSO: Conexão funcionando!")
        print("🎯 Agora você pode usar SQL Server com Python")
    else:
        print("\n❌ ERRO: Verifique configurações")
        print("📋 Possíveis soluções:")
        print("   1. Configure firewall no Azure")
        print("   2. Verifique credenciais")
        print("   3. Use extensão SQL no VS Code")