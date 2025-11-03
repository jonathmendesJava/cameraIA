# 📦 Guia Completo de Instalação - Face Recognition API

## 📋 Índice

1. [Requisitos do Sistema](#requisitos-do-sistema)
2. [Instalação do Python](#instalação-do-python)
3. [Ferramentas de Desenvolvimento (Windows)](#ferramentas-de-desenvolvimento-windows)
4. [Clone e Configuração do Projeto](#clone-e-configuração-do-projeto)
5. [Instalação de Dependências Python](#instalação-de-dependências-python)
6. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
7. [Variáveis de Ambiente](#variáveis-de-ambiente)
8. [Instalação do face-recognition (Opcional mas Recomendado)](#instalação-do-face-recognition-opcional-mas-recomendado)
9. [Verificação da Instalação](#verificação-da-instalação)
10. [Executando o Projeto](#executando-o-projeto)
11. [Troubleshooting](#troubleshooting)

---

## 🖥️ Requisitos do Sistema

### Mínimos
- **Sistema Operacional**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **RAM**: 4GB (recomendado 8GB+)
- **Espaço em Disco**: 5GB livres (para dependências e compilação)
- **Processador**: Dual-core 2.0GHz+

### Recomendados
- **RAM**: 8GB ou mais
- **Espaço em Disco**: 10GB+ livres
- **Processador**: Quad-core ou superior
- **Webcam**: Para funcionalidade de reconhecimento em tempo real
- **GPU**: Opcional, mas melhora performance em reconhecimento facial

---

## 🐍 Instalação do Python

### Windows

1. **Baixar Python**
   - Acesse: https://www.python.org/downloads/
   - Baixe a versão **Python 3.11 ou superior**
   - ⚠️ **IMPORTANTE**: Marque a opção **"Add Python to PATH"** durante a instalação

2. **Verificar Instalação**
   ```powershell
   python --version
   # Deve mostrar: Python 3.11.x ou superior
   
   pip --version
   # Deve mostrar: pip 23.x ou superior
   ```

### Linux (Ubuntu/Debian)

```bash
# Atualizar pacotes
sudo apt update

# Instalar Python e pip
sudo apt install python3.11 python3.11-venv python3-pip -y

# Verificar instalação
python3.11 --version
pip3 --version
```

### macOS

```bash
# Usando Homebrew (recomendado)
brew install python@3.11

# Ou baixar direto de: https://www.python.org/downloads/macos/
```

---

## 🔧 Ferramentas de Desenvolvimento (Windows)

⚠️ **Obrigatório apenas se você quiser instalar o `face-recognition`**

### 1. CMake

1. **Download**
   - Acesse: https://cmake.org/download/
   - Baixe o instalador Windows (.msi)

2. **Instalação**
   - Execute o instalador
   - ⚠️ **CRÍTICO**: Marque a opção **"Add CMake to system PATH for all users"** ou **"Add CMake to system PATH for current user"**
   - Clique em "Install"

3. **Verificação**
   ```powershell
   # Reinicie o terminal e execute:
   cmake --version
   # Deve mostrar: cmake version 3.x.x ou superior
   ```

### 2. Visual Studio Build Tools (ou Visual Studio Community)

#### Opção A: Build Tools (Mais Leve)

1. **Download**
   - Acesse: https://visualstudio.microsoft.com/downloads/
   - Role até "All downloads" → "Tools for Visual Studio"
   - Baixe "Build Tools for Visual Studio 2022"

2. **Instalação**
   - Execute o instalador
   - Selecione o workload: **"Desktop development with C++"**
   - Em "Installation details", certifique-se de que estão marcados:
     - ✅ MSVC v143 - VS 2022 C++ x64/x86 build tools
     - ✅ Windows 10/11 SDK (última versão)
     - ✅ CMake tools for Windows
   - Clique em "Install"

#### Opção B: Visual Studio Community (Mais Completo)

1. **Download**
   - Acesse: https://visualstudio.microsoft.com/downloads/
   - Baixe "Visual Studio Community 2022"

2. **Instalação**
   - Execute o instalador
   - Selecione o workload: **"Desktop development with C++"**
   - Clique em "Install"

3. **Verificação**
   ```powershell
   # Verificar se compilador está disponível
   cl
   # Deve mostrar informações do compilador ou erro de sintaxe (isso é normal)
   ```

---

## 📥 Clone e Configuração do Projeto

### 1. Clonar o Repositório

```bash
# Via Git
git clone <URL_DO_REPOSITORIO>
cd film.ai

# Ou baixar ZIP e extrair
```

### 2. Criar Ambiente Virtual

#### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Windows (CMD)
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Atualizar pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

---

## 📚 Instalação de Dependências Python

### Dependências Básicas (Obrigatórias)

Todas essas bibliotecas estão no `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### Lista Completa de Dependências:

| Biblioteca | Versão | Descrição |
|------------|--------|-----------|
| **fastapi** | 0.104.1 | Framework web moderno e rápido para APIs REST |
| **uvicorn[standard]** | 0.24.0 | Servidor ASGI de alta performance |
| **python-multipart** | 0.0.6 | Suporte a upload de arquivos (multipart/form-data) |
| **opencv-python** | 4.8.1.78 | Biblioteca de visão computacional |
| **numpy** | 1.24.3 | Computação numérica e arrays multidimensionais |
| **Pillow** | 10.1.0 | Processamento de imagens |
| **SQLAlchemy** | 2.0.23 | ORM para banco de dados |
| **pydantic** | 2.5.0 | Validação de dados e modelos |
| **python-dotenv** | 1.0.0 | Carregar variáveis de ambiente de arquivo .env |
| **httpx** | 0.25.2 | Cliente HTTP para webhooks e APIs |

#### Dependências Automáticas (instaladas com as acima):

| Biblioteca | Versão | Descrição |
|------------|--------|-----------|
| **anyio** | ~3.7.1 | Biblioteca de async/await |
| **starlette** | ~0.27.0 | Framework ASGI (base do FastAPI) |
| **click** | ~8.3.0 | CLI framework |
| **colorama** | ~0.4.6 | Cores no terminal (Windows) |
| **greenlet** | ~3.2.4 | Suporte a greenlets |
| **h11** | ~0.16.0 | Implementação HTTP/1.1 |
| **httptools** | ~0.7.1 | Parsing HTTP otimizado |
| **httpcore** | ~1.0.9 | Core HTTP client |
| **idna** | ~3.11 | Suporte a nomes de domínio internacionais |
| **typing-extensions** | ~4.15.0 | Extensões de type hints |
| **websockets** | ~15.0.1 | Suporte a WebSockets |
| **watchfiles** | ~1.1.1 | Monitoramento de arquivos |
| **pyyaml** | ~6.0.3 | Parser YAML |
| **certifi** | ~2025.10.5 | Certificados CA para SSL |
| **sniffio** | ~1.3.1 | Detecção de biblioteca async |

### Dependências Opcionais (face-recognition)

⚠️ **Requer CMake e Visual Studio Build Tools no Windows**

```bash
pip install dlib
pip install face-recognition==1.3.0
```

Ou use o script automatizado:
```powershell
# Windows PowerShell
.\install-face-recognition.ps1
```

---

## 🗄️ Configuração do Banco de Dados

### SQLite (Padrão - Não Requer Instalação)

O SQLite é incluído no Python e é criado automaticamente na primeira execução.

- **Localização padrão**: `data/face_recognition.db`
- **Configurável via**: Variável de ambiente `DATABASE_PATH`

### Criar Diretório de Dados

O diretório `data/` é criado automaticamente, mas você pode criar manualmente:

```bash
mkdir data
```

---

## 🔐 Variáveis de Ambiente

### Criar Arquivo .env

Crie um arquivo `.env` na raiz do projeto:

```env
# API Key para autenticação (MUDE EM PRODUÇÃO!)
API_KEY=your-secret-api-key-123

# URL do webhook para notificações (opcional)
WEBHOOK_URL=https://seu-webhook-url.com/notify

# Caminho do banco de dados (opcional)
DATABASE_PATH=data/face_recognition.db

# Habilitar logs SQL (para debug, opcional)
DB_ECHO=false
```

### Segurança

⚠️ **IMPORTANTE**: 
- **NUNCA** commite o arquivo `.env` no Git
- Use uma API key forte em produção
- O `.env.example` mostra o formato sem valores reais

---

## 🧠 Instalação do face-recognition (Opcional mas Recomendado)

### Windows - Passo a Passo

1. **Instalar CMake** (já explicado acima)
2. **Instalar Visual Studio Build Tools** (já explicado acima)
3. **Reiniciar o Terminal**
4. **Executar Instalação**:

```powershell
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar dlib (pode levar vários minutos)
pip install dlib

# Instalar face-recognition
pip install face-recognition==1.3.0
```

### Linux

```bash
# Instalar dependências do sistema
sudo apt-get update
sudo apt-get install cmake libopenblas-dev liblapack-dev libjpeg-dev libpng-dev

# Ativar ambiente virtual
source venv/bin/activate

# Instalar
pip install dlib
pip install face-recognition==1.3.0
```

### macOS

```bash
# Instalar dependências via Homebrew
brew install cmake dlib

# Ativar ambiente virtual
source venv/bin/activate

# Instalar
pip install dlib
pip install face-recognition==1.3.0
```

### Verificação

```python
python -c "import face_recognition; print('✅ face-recognition instalado!')"
```

---

## ✅ Verificação da Instalação

### Script de Verificação

Crie um arquivo `verify_install.py`:

```python
import sys

def check_package(name, import_name=None):
    """Verifica se um pacote está instalado"""
    if import_name is None:
        import_name = name
    try:
        __import__(import_name)
        print(f"✅ {name}")
        return True
    except ImportError:
        print(f"❌ {name} - NÃO INSTALADO")
        return False

print("=" * 50)
print("VERIFICAÇÃO DE INSTALAÇÃO")
print("=" * 50)

packages = [
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
    ("opencv-python", "cv2"),
    ("numpy", "numpy"),
    ("Pillow", "PIL"),
    ("SQLAlchemy", "sqlalchemy"),
    ("pydantic", "pydantic"),
    ("face-recognition", "face_recognition"),  # Opcional
]

all_ok = True
for pkg_name, import_name in packages:
    if not check_package(pkg_name, import_name):
        all_ok = False

print("=" * 50)
if all_ok:
    print("✅ TODAS AS DEPENDÊNCIAS ESTÃO INSTALADAS!")
else:
    print("⚠️  ALGUMAS DEPENDÊNCIAS ESTÃO FALTANDO")
    print("Execute: pip install -r requirements.txt")
print("=" * 50)
```

Execute:
```bash
python verify_install.py
```

---

## 🚀 Executando o Projeto

### 1. Ativar Ambiente Virtual

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/macOS
source venv/bin/activate
```

### 2. Iniciar o Servidor

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Acessar a API

- **API**: http://localhost:8000
- **Documentação Interativa**: http://localhost:8000/docs
- **Documentação Alternativa**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 4. Testar Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Status (sem auth)
curl http://localhost:8000/status

# Status com API key
curl -H "x-api-key: your-secret-api-key-123" http://localhost:8000/status
```

---

## 🔍 Troubleshooting

### Problema: Python não encontrado

**Solução:**
```powershell
# Windows: Adicione Python ao PATH
# Durante instalação, marque "Add Python to PATH"
# Ou adicione manualmente: C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python311\
```

### Problema: pip não encontrado

**Solução:**
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Problema: CMake não encontrado após instalação

**Solução:**
```powershell
# Reinicie o terminal completamente
# Ou adicione manualmente ao PATH:
# C:\Program Files\CMake\bin
```

### Problema: Erro ao compilar dlib

**Causas Comuns:**
1. CMake não está no PATH
2. Visual Studio Build Tools não está instalado
3. Terminal não foi reiniciado após instalar ferramentas

**Solução:**
```powershell
# 1. Verificar CMake
cmake --version

# 2. Verificar compilador
# Abra "Developer Command Prompt for VS" e tente novamente

# 3. Ou use conda como alternativa
conda install -c conda-forge dlib
```

### Problema: "Microsoft Visual C++ 14.0 or greater is required"

**Solução:**
- Instale Visual Studio Build Tools com workload "Desktop development with C++"
- Reinicie o computador após instalação
- Abra um novo terminal

### Problema: Câmera não funciona

**Soluções:**
```python
# Verificar se OpenCV detecta câmeras
python -c "import cv2; print([i for i in range(5) if cv2.VideoCapture(i).isOpened()])"

# Pode precisar ajustar o índice da câmera em camera_service.py
```

### Problema: Banco de dados travado

**Solução:**
```bash
# Verificar se outro processo está usando
# Fechar todas as conexões
# Ou deletar e recriar: rm data/face_recognition.db
```

### Problema: Porta 8000 já em uso

**Solução:**
```bash
# Usar outra porta
python -m uvicorn app.main:app --reload --port 8001

# Ou matar processo na porta 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problema: Erro de importação de módulos

**Solução:**
```bash
# Certifique-se de estar no diretório raiz do projeto
# E com ambiente virtual ativado
pwd  # Linux/macOS
cd   # Windows
```

---

## 📦 Resumo Rápido - Checklist de Instalação

### Windows - Checklist Completo

- [ ] Instalar Python 3.11+ (marcar "Add to PATH")
- [ ] Instalar CMake (marcar "Add to PATH")
- [ ] Instalar Visual Studio Build Tools com "Desktop development with C++"
- [ ] Reiniciar terminal/computador
- [ ] Clonar repositório
- [ ] Criar ambiente virtual: `python -m venv venv`
- [ ] Ativar ambiente: `.\venv\Scripts\Activate.ps1`
- [ ] Atualizar pip: `python -m pip install --upgrade pip`
- [ ] Instalar dependências: `pip install -r requirements.txt`
- [ ] Criar arquivo `.env` com configurações
- [ ] (Opcional) Instalar face-recognition: `pip install dlib face-recognition`
- [ ] Iniciar servidor: `python -m uvicorn app.main:app --reload`
- [ ] Acessar http://localhost:8000/docs

### Linux/macOS - Checklist Completo

- [ ] Instalar Python 3.11+
- [ ] Instalar cmake: `sudo apt install cmake` (Linux) ou `brew install cmake` (macOS)
- [ ] Clonar repositório
- [ ] Criar ambiente virtual: `python3 -m venv venv`
- [ ] Ativar ambiente: `source venv/bin/activate`
- [ ] Atualizar pip: `pip install --upgrade pip`
- [ ] Instalar dependências: `pip install -r requirements.txt`
- [ ] Criar arquivo `.env`
- [ ] (Opcional) Instalar face-recognition: `pip install dlib face-recognition`
- [ ] Iniciar servidor: `python -m uvicorn app.main:app --reload`
- [ ] Acessar http://localhost:8000/docs

---

## 📚 Recursos Adicionais

### Documentação Oficial

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **face-recognition**: https://github.com/ageitgey/face_recognition
- **OpenCV**: https://opencv.org/
- **Uvicorn**: https://www.uvicorn.org/

### Comandos Úteis

```bash
# Listar pacotes instalados
pip list

# Verificar dependências
pip check

# Gerar requirements atualizado
pip freeze > requirements-current.txt

# Atualizar todas as dependências
pip install --upgrade -r requirements.txt

# Ver informações de um pacote
pip show fastapi

# Desinstalar tudo e reinstalar
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## 🎯 Próximos Passos Após Instalação

1. ✅ Verificar instalação com `verify_install.py`
2. ✅ Configurar arquivo `.env`
3. ✅ Iniciar servidor
4. ✅ Testar endpoints em http://localhost:8000/docs
5. ✅ Treinar primeiro rosto via `/train`
6. ✅ Testar reconhecimento via `/recognize/image`
7. ✅ (Opcional) Iniciar reconhecimento em tempo real via `/recognize/start`

---

## 💡 Dicas de Performance

- Use SSD para melhor performance do banco de dados
- Para produção, considere PostgreSQL ao invés de SQLite
- Use GPU se disponível para processamento mais rápido
- Configure pool de conexões adequadamente
- Faça backups regulares do banco de dados

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs do servidor
2. Confira o arquivo de troubleshooting acima
3. Verifique versões de Python e dependências
4. Consulte a documentação oficial das bibliotecas
5. Verifique issues no repositório do projeto

---

**Última atualização**: Janeiro 2025
**Versão do projeto**: 1.0.0
