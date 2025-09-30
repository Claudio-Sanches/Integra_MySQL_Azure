"""
Script de limpeza do projeto para GitHub
Remove arquivos temporários e sensíveis
"""
import os
import shutil
import glob

def cleanup_project():
    """Remove arquivos temporários e prepara para GitHub"""
    print("🧹 LIMPEZA DO PROJETO PARA GITHUB")
    print("=" * 40)
    
    # Arquivos/pastas para remover
    items_to_remove = [
        # Cache Python
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        
        # Logs
        "*.log",
        "logs/",
        
        # Temporários
        "*.tmp",
        "*.temp",
        "*~",
        "*.bak",
        
        # IDE
        ".vscode/settings.json",  # Manter apenas template
        ".idea/",
        
        # Sistema
        "Thumbs.db",
        ".DS_Store",
        
        # Backups locais
        "*_backup.*",
        "backup_*",
    ]
    
    removed_count = 0
    
    for pattern in items_to_remove:
        # Buscar arquivos/pastas que correspondem ao padrão
        matches = glob.glob(pattern, recursive=True)
        
        for item in matches:
            try:
                if os.path.isfile(item):
                    os.remove(item)
                    print(f"  🗑️ Removido arquivo: {item}")
                    removed_count += 1
                elif os.path.isdir(item):
                    shutil.rmtree(item)
                    print(f"  📁 Removida pasta: {item}")
                    removed_count += 1
            except Exception as e:
                print(f"  ⚠️ Erro ao remover {item}: {e}")
    
    print(f"\n✅ Limpeza concluída: {removed_count} itens removidos")
    return removed_count

def secure_sensitive_files():
    """Protege arquivos sensíveis"""
    print(f"\n🔒 VERIFICAÇÃO DE ARQUIVOS SENSÍVEIS")
    print("=" * 40)
    
    sensitive_files = [
        ".env",
        "config/settings.py",
        "credentials.json",
        "secrets.json",
    ]
    
    found_sensitive = []
    
    for file in sensitive_files:
        if os.path.exists(file):
            found_sensitive.append(file)
            print(f"  ⚠️ ARQUIVO SENSÍVEL ENCONTRADO: {file}")
    
    if found_sensitive:
        print(f"\n❌ ATENÇÃO: {len(found_sensitive)} arquivo(s) sensível(is) encontrado(s)!")
        print("🔐 Certifique-se de que estão no .gitignore antes do commit!")
        
        for file in found_sensitive:
            print(f"  🚨 {file}")
    else:
        print(f"  ✅ Nenhum arquivo sensível detectado")
    
    return found_sensitive

def create_env_template():
    """Cria template do arquivo .env para outros desenvolvedores"""
    template_content = """# ===============================================
# TEMPLATE - Configurações do SQL Server Azure
# ===============================================
# INSTRUÇÕES:
# 1. Copie este arquivo para .env
# 2. Substitua os valores pelos seus dados reais
# 3. NUNCA commite o arquivo .env real

# Servidor SQL Server (encontre no portal do Azure)
MYSQL_HOST=seu-servidor.database.windows.net

# Nome do banco de dados
MYSQL_DATABASE=seu-banco

# Usuário (formato: usuario ou usuario@servidor)
MYSQL_USER=seu-usuario

# Senha do banco (MANTENHA SEGURA!)
MYSQL_PASSWORD=sua-senha-aqui

# Porta do SQL Server (padrão: 1433)
MYSQL_PORT=1433

# Certificado SSL (se necessário)
MYSQL_SSL_CA=DigiCertGlobalRootCA.crt.pem
"""
    
    try:
        with open('.env.template', 'w', encoding='utf-8') as f:
            f.write(template_content)
        print(f"  ✅ Criado: .env.template")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao criar .env.template: {e}")
        return False

def create_vscode_settings():
    """Cria configurações VS Code recomendadas"""
    vscode_settings = {
        "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.formatting.provider": "black",
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True,
            ".env": True
        },
        "python.analysis.extraPaths": [
            "./config",
            "./database", 
            "./utils"
        ]
    }
    
    os.makedirs('.vscode', exist_ok=True)
    
    try:
        import json
        with open('.vscode/settings.json', 'w', encoding='utf-8') as f:
            json.dump(vscode_settings, f, indent=2)
        print(f"  ✅ Criado: .vscode/settings.json")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao criar configurações VS Code: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PREPARAÇÃO PARA GITHUB")
    print("=" * 50)
    
    # Executar limpeza
    cleanup_project()
    
    # Verificar arquivos sensíveis
    sensitive_files = secure_sensitive_files()
    
    # Criar templates
    print(f"\n📝 CRIAÇÃO DE TEMPLATES")
    print("=" * 30)
    create_env_template()
    create_vscode_settings()
    
    # Resumo final
    print(f"\n🎯 RESUMO DA PREPARAÇÃO")
    print("=" * 30)
    print(f"  🧹 Limpeza realizada")
    print(f"  📝 Templates criados")
    print(f"  🔒 .gitignore recomendado disponível")
    
    if sensitive_files:
        print(f"\n❌ AÇÃO NECESSÁRIA:")
        print(f"  🔐 Verifique arquivos sensíveis antes do commit!")
    else:
        print(f"\n✅ PROJETO PRONTO PARA GITHUB!")
    
    print(f"\n🚀 PRÓXIMOS PASSOS:")
    print(f"  1. Adicione o .gitignore")
    print(f"  2. Execute: git init")
    print(f"  3. Execute: git add .")
    print(f"  4. Execute: git commit -m 'Initial commit'")
    print(f"  5. Crie repositório no GitHub")
    print(f"  6. Execute: git remote add origin <URL>")
    print(f"  7. Execute: git push -u origin main")