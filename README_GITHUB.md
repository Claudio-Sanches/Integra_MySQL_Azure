# 📊 Dashboard Corporativo - MySQL & Azure Integration

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Azure](https://img.shields.io/badge/Azure-SQL%20Database-blue.svg)](https://azure.microsoft.com)
[![Power BI](https://img.shields.io/badge/Power%20BI-Integration-yellow.svg)](https://powerbi.microsoft.com)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)]()

Sistema modular Python para criação automatizada do banco **Company** no **Azure SQL Server** com integração **Power BI** e **8 views especializadas**.

## 🎯 Características Principais

- 🏗️ **Arquitetura Modular** - Código organizado e reutilizável
- 🌐 **Azure SQL Database** - Infraestrutura cloud escalável  
- 📊 **Views Power BI** - 8 demandas específicas atendidas
- 🚀 **Automação Completa** - Script único para criação total
- 🧪 **Testes Integrados** - Validação automática de integridade
- 📚 **Documentação Completa** - README detalhado + screenshots Azure

## 🚀 Quick Start

### 1. Instalação
```bash
git clone https://github.com/seu-usuario/dashboard-mysql-azure.git
cd dashboard-mysql-azure
pip install -r requirements.txt
```

### 2. Configuração
```bash
# Copie e configure suas credenciais
cp .env.template .env
# Edite .env com suas credenciais Azure
```

### 3. Execução
```bash
# Cria todo o ambiente automaticamente
python main.py
```

## 📁 Estrutura Modular

```
📁 config/          # Configurações e credenciais
📁 database/        # Módulos especializados
├── connection.py   # Gerenciamento de conexão
├── schema.py       # Criação de tabelas
├── data.py         # Inserção de dados
├── views.py        # Views Power BI
└── validation.py   # Testes e validação
📁 utils/           # Funções auxiliares
main.py             # 🎯 Script principal
```

## 📊 Views Power BI Implementadas

| Demanda | View Criada | Funcionalidade |
|---------|-------------|----------------|
| 9-11 | `vw_employee_manager` | Funcionários + departamentos + gerentes |
| 13 | `vw_department_location` | Departamentos mesclados com localizações |
| 15 | `vw_employees_by_manager` | Agrupamento por gerente |
| 16 | `vw_powerbi_final` | View otimizada final |

## 🌐 Infraestrutura Azure

### Configuração Necessária
- **Azure SQL Database**
- **Firewall configurado** para seu IP
- **Credenciais** no arquivo `.env`

### Exemplo de Configuração
```env
MYSQL_HOST=seu-servidor.database.windows.net
MYSQL_DATABASE=seu-banco
MYSQL_USER=seu-usuario
MYSQL_PASSWORD=sua-senha
MYSQL_PORT=1433
```

## 🧪 Testes

```bash
# Teste da estrutura modular
python teste_completo.py

# Teste de imports
python test_imports.py
```

## 📈 Resultados

```bash
🎉 BANCO COMPANY CRIADO COM SUCESSO!
✅ 6 tabelas, 4 views Power BI, 47 registros
📊 Sistema 100% funcional e validado
```

## 🛠️ Tecnologias

- **Python 3.8+** - Linguagem principal
- **pymssql** - Driver SQL Server
- **Azure SQL Database** - Banco de dados cloud
- **Power BI** - Visualização de dados
- **Arquitetura Modular** - Organização profissional

## 📚 Documentação

- 📋 [`README.md`](README.md) - Documentação técnica completa
- 📊 [`resumo.md`](resumo.md) - Resumo executivo
- 🌐 [`Ambiente Azure/`](Ambiente%20Azure/) - Screenshots configuração

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja [`LICENSE`](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Claudio B Sanches**
- 📧 Email: [seu-email@example.com]
- 💼 LinkedIn: [seu-linkedin]
- 🌐 GitHub: [@seu-usuario]

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐