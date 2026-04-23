"""
check_setup.py
Script para verificar se o ambiente está configurado corretamente.
Útil para diagnosticar problemas.
"""

import sys
import os
from pathlib import Path

print("=" * 60)
print("🔍 VERIFICANDO CONFIGURAÇÃO DO SISTEMA")
print("=" * 60)

# Verificar versão do Python
print(f"\n✓ Versão Python: {sys.version}")
if sys.version_info < (3, 12):
    print("  ⚠️  Aviso: Python 3.12+ recomendado")
else:
    print("  ✅ Python OK")

# Verificar pacotes instalados
print("\n📦 VERIFICANDO PACOTES...")

pacotes_necessarios = {
    'flask': 'Flask (servidor web)',
    'requests': 'Requests (HTTP)',
    'groq': 'Groq (IA)',
    'pytest': 'Pytest (testes)',
    'flake8': 'Flake8 (linting)',
    'sqlite3': 'SQLite3 (banco de dados)',
}

todos_ok = True
for pacote, descricao in pacotes_necessarios.items():
    try:
        __import__(pacote)
        print(f"  ✅ {pacote:15} - {descricao}")
    except ImportError:
        print(f"  ❌ {pacote:15} - {descricao} (NÃO INSTALADO)")
        todos_ok = False

# Verificar arquivos principais
print("\n📁 VERIFICANDO ARQUIVOS...")

arquivos_necessarios = [
    'app.py',
    'main.py',
    'medicamentos.py',
    'database.py',
    'api_integration.py',
    'requirements.txt',
    'templates/index.html',
    'static/style.css',
    'static/script.js',
    '.env.example',
]

for arquivo in arquivos_necessarios:
    caminho = Path(arquivo)
    if caminho.exists():
        tamanho = caminho.stat().st_size
        print(f"  ✅ {arquivo:30} ({tamanho} bytes)")
    else:
        print(f"  ❌ {arquivo:30} (FALTANDO)")
        todos_ok = False

# Verificar banco de dados
print("\n💾 VERIFICANDO BANCO DE DADOS...")
if Path('medicamentos.db').exists():
    print(f"  ✅ medicamentos.db existe")
    # Verificar se as tabelas existem
    try:
        import sqlite3
        conn = sqlite3.connect('medicamentos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = cursor.fetchall()
        print(f"  ✅ Tabelas encontradas: {len(tabelas)}")
        for tabela in tabelas:
            print(f"     - {tabela[0]}")
        conn.close()
    except Exception as e:
        print(f"  ⚠️  Erro ao verificar banco: {e}")
else:
    print(f"  ℹ️  medicamentos.db não existe (será criado ao iniciar)")

# Verificar variáveis de ambiente
print("\n🔐 VERIFICANDO CONFIGURAÇÕES...")
if Path('.env').exists():
    print(f"  ✅ Arquivo .env encontrado")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key and groq_key != 'your_groq_api_key_here':
            print(f"  ✅ GROQ_API_KEY configurada")
        else:
            print(f"  ℹ️  GROQ_API_KEY não configurada (opcional)")
    except Exception as e:
        print(f"  ⚠️  Erro ao carregar .env: {e}")
else:
    print(f"  ℹ️  Arquivo .env não existe (usando padrões)")

# Resumo final
print("\n" + "=" * 60)
if todos_ok:
    print("✅ TUDO PARECE ESTAR OK!")
    print("\nPróximas etapas:")
    print("1. Execute: python app.py")
    print("2. Abra seu navegador em: http://localhost:5000")
else:
    print("⚠️  ALGUNS PROBLEMAS FORAM DETECTADOS")
    print("\nExecute:")
    print("  pip install -r requirements.txt")
    print("\nDepois tente novamente este script.")

print("=" * 60)
