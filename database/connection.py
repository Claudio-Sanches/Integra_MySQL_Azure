"""
Gerenciamento de conexão com o banco de dados
"""
import pymssql
from config.settings import DatabaseConfig
from config.constants import MESSAGES

class DatabaseConnection:
    """Classe para gerenciar conexão com SQL Server"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Estabelece conexão com o banco"""
        try:
            print(MESSAGES['connecting'])
            
            # Validar configurações
            DatabaseConfig.validate_config()
            
            # Conectar
            self.connection = pymssql.connect(**DatabaseConfig.get_connection_params())
            self.cursor = self.connection.cursor()
            
            print(MESSAGES['connected'])
            return True
            
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False
    
    def disconnect(self):
        """Fecha a conexão com o banco"""
        if self.connection:
            self.connection.close()
            print(MESSAGES['closed'])
    
    def get_cursor(self):
        """Retorna o cursor para executar comandos"""
        if not self.cursor:
            raise ConnectionError("Não há conexão ativa com o banco")
        return self.cursor
    
    def __enter__(self):
        """Context manager - entrada"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager - saída"""
        self.disconnect()