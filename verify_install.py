#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificação de instalação
Verifica se todas as dependências necessárias estão instaladas
"""

import sys
import os

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def check_package(name, import_name=None, required=True):
    """Verifica se um pacote está instalado"""
    if import_name is None:
        import_name = name
    
    try:
        __import__(import_name)
        print(f"✅ {name:25s} - INSTALADO")
        return True
    except ImportError:
        status = "❌ REQUERIDO" if required else "⚠️  OPCIONAL"
        print(f"{status} {name:25s} - NÃO INSTALADO")
        return False

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - REQUER PYTHON 3.11+")
        return False

def check_file_exists(path, name):
    """Verifica se arquivo existe"""
    if os.path.exists(path):
        print(f"✅ {name:25s} - ENCONTRADO")
        return True
    else:
        print(f"⚠️  {name:25s} - NÃO ENCONTRADO (será criado automaticamente)")
        return False

def check_env_file():
    """Verifica se arquivo .env existe"""
    if os.path.exists('.env'):
        print(f"✅ .env                     - ENCONTRADO")
        return True
    else:
        print(f"⚠️  .env                     - NÃO ENCONTRADO (crie um baseado em .env.example)")
        return False

def main():
    print("=" * 70)
    print(" " * 15 + "VERIFICAÇÃO DE INSTALAÇÃO")
    print("=" * 70)
    print()
    
    all_ok = True
    
    # Verificar Python
    print("📦 VERIFICANDO PYTHON:")
    print("-" * 70)
    if not check_python_version():
        all_ok = False
    print()
    
    # Verificar pacotes obrigatórios
    print("📚 VERIFICANDO DEPENDÊNCIAS OBRIGATÓRIAS:")
    print("-" * 70)
    required_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("opencv-python", "cv2"),
        ("numpy", "numpy"),
        ("Pillow", "PIL"),
        ("SQLAlchemy", "sqlalchemy"),
        ("pydantic", "pydantic"),
        ("python-multipart", None),  # Não precisa importar
        ("python-dotenv", "dotenv"),
        ("httpx", "httpx"),
    ]
    
    for pkg_name, import_name in required_packages:
        if import_name and not check_package(pkg_name, import_name, required=True):
            all_ok = False
    
    print()
    
    # Verificar pacotes opcionais
    print("🔧 VERIFICANDO DEPENDÊNCIAS OPCIONAIS:")
    print("-" * 70)
    optional_packages = [
        ("face-recognition", "face_recognition"),
        ("dlib", "dlib"),
    ]
    
    optional_ok = True
    for pkg_name, import_name in optional_packages:
        if not check_package(pkg_name, import_name, required=False):
            optional_ok = False
    
    print()
    
    # Verificar arquivos do projeto
    print("📁 VERIFICANDO ESTRUTURA DO PROJETO:")
    print("-" * 70)
    files_to_check = [
        ("app/main.py", "app/main.py"),
        ("app/database.py", "app/database.py"),
        ("requirements.txt", "requirements.txt"),
    ]
    
    for path, name in files_to_check:
        check_file_exists(path, name)
    
    print()
    
    # Verificar .env
    print("🔐 VERIFICANDO CONFIGURAÇÕES:")
    print("-" * 70)
    check_env_file()
    print()
    
    # Verificar diretórios
    dirs_to_check = ["app", "app/routes", "app/services", "data"]
    print("📂 VERIFICANDO DIRETÓRIOS:")
    print("-" * 70)
    for dir_path in dirs_to_check:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path:25s} - EXISTE")
        else:
            print(f"⚠️  {dir_path:25s} - NÃO EXISTE (será criado automaticamente)")
    print()
    
    # Resultado final
    print("=" * 70)
    if all_ok:
        print("✅ TODAS AS DEPENDÊNCIAS OBRIGATÓRIAS ESTÃO INSTALADAS!")
        if optional_ok:
            print("✅ TODAS AS DEPENDÊNCIAS OPCIONAIS TAMBÉM ESTÃO INSTALADAS!")
        else:
            print("⚠️  ALGUMAS DEPENDÊNCIAS OPCIONAIS ESTÃO FALTANDO")
            print("   (face-recognition requer CMake e Visual Studio Build Tools)")
            print("   Veja INSTALACAO_COMPLETA.md para mais detalhes")
        print()
        print("🚀 Você pode iniciar o servidor com:")
        print("   python -m uvicorn app.main:app --reload")
    else:
        print("❌ ALGUMAS DEPENDÊNCIAS OBRIGATÓRIAS ESTÃO FALTANDO!")
        print()
        print("📝 Para instalar todas as dependências, execute:")
        print("   pip install -r requirements.txt")
    print("=" * 70)
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
