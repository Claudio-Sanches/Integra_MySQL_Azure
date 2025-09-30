"""
Funções auxiliares e utilitários
"""

def execute_command(cursor, command, description):
    """
    Executa um comando SQL único com tratamento de erro
    
    Args:
        cursor: Cursor do banco de dados
        command: Comando SQL a ser executado
        description: Descrição da operação
    
    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        cursor.execute(command)
        print(f"  ✅ {description}")
        return True
    except Exception as e:
        error_msg = str(e)[:100] + "..." if len(str(e)) > 100 else str(e)
        print(f"  ❌ {description}: {error_msg}")
        return False

def print_header(title):
    """Imprime cabeçalho formatado"""
    print(f"\n{title}")
    print("=" * len(title))

def print_section(message):
    """Imprime seção formatada"""
    print(f"\n{message}")

def format_currency(value):
    """Formata valor como moeda"""
    return f"${value:,.2f}"

def execute_multiple_commands(cursor, commands_dict, section_name):
    """
    Executa múltiplos comandos SQL
    
    Args:
        cursor: Cursor do banco de dados
        commands_dict: Dicionário {descrição: comando_sql}
        section_name: Nome da seção para logging
    
    Returns:
        int: Número de comandos executados com sucesso
    """
    print(f"\n{section_name}")
    success_count = 0
    
    for description, command in commands_dict.items():
        if execute_command(cursor, command, description):
            success_count += 1
    
    return success_count