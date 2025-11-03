# ⚡ Quick Start - Guia Rápido

## 🚀 Início Rápido (5 minutos)

### Pré-requisitos Mínimos

- Python 3.11+ instalado
- pip atualizado
- Git (para clonar)

### Passos Rápidos

```bash
# 1. Clonar repositório
git clone <URL_DO_REPOSITORIO>
cd film.ai

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/macOS:
source venv/bin/activate

# 4. Instalar dependências básicas
pip install --upgrade pip
pip install -r requirements.txt

# 5. Criar arquivo .env
copy .env.example .env  # Windows
# ou
cp .env.example .env    # Linux/macOS
# Edite o .env e configure sua API_KEY

# 6. Iniciar servidor
python -m uvicorn app.main:app --reload

# 7. Acessar documentação
# Abra no navegador: http://localhost:8000/docs
```

### Verificar Instalação

```bash
python verify_install.py
```

## ✅ Pronto!

Agora você pode:
- ✅ Testar endpoints em http://localhost:8000/docs
- ✅ Verificar status: http://localhost:8000/status
- ✅ Começar a usar a API!

## 📖 Documentação Completa

Para instalação completa com todas as ferramentas (CMake, Visual Studio, etc), veja:
- **[INSTALACAO_COMPLETA.md](INSTALACAO_COMPLETA.md)** - Guia detalhado passo a passo

## ⚠️ Funcionalidades Avançadas

Para usar reconhecimento facial completo, você também precisa:
- CMake
- Visual Studio Build Tools (Windows)
- face-recognition library

Veja [INSTALACAO_COMPLETA.md](INSTALACAO_COMPLETA.md) para detalhes.
