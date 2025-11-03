# 🎭 Face Recognition API

API de reconhecimento facial em tempo real usando FastAPI e visão computacional. Sistema completo para treinar rostos e reconhecê-los via streaming de câmera com sistema de alertas.

## 📚 Documentação Completa

- **[INSTALACAO_COMPLETA.md](INSTALACAO_COMPLETA.md)** - 📦 **Guia completo de instalação** com todas as dependências, ferramentas e tecnologias necessárias
- **[DATABASE_CONFIG.md](DATABASE_CONFIG.md)** - 🗄️ Configuração e uso do banco de dados
- **[INSTALL_INSTRUCTIONS.md](INSTALL_INSTRUCTIONS.md)** - 🔧 Instruções específicas para instalar face-recognition

> ⚠️ **NOVO NO PROJETO?** Comece pelo arquivo [INSTALACAO_COMPLETA.md](INSTALACAO_COMPLETA.md) para uma instalação completa do zero!

## 🚀 Funcionalidades

- ✅ Treinamento de rostos via upload de imagem
- ✅ Reconhecimento facial em tempo real via streaming de câmera
- ✅ Banco de dados SQLite para armazenar rostos treinados
- ✅ Sistema de alertas via webhook
- ✅ API REST completa documentada
- ✅ Segurança via API Key

## 📋 Pré-requisitos

### Windows
1. **Python 3.11+** (já instalado ✓)
2. **CMake** (necessário para dlib):
   - Download: https://cmake.org/download/
   - **Importante**: Durante a instalação, marque a opção "Add CMake to system PATH"
   - Reinicie o terminal após instalar

3. **Visual Studio Build Tools** (ou Visual Studio Community):
   - Download: https://visualstudio.microsoft.com/downloads/
   - Selecione "Desktop development with C++" workload
   - Ou instale apenas as Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

## 🔧 Instalação

> 💡 **Dica**: Para instalação completa e detalhada de TODAS as dependências, ferramentas e tecnologias, consulte **[INSTALACAO_COMPLETA.md](INSTALACAO_COMPLETA.md)**

### Quick Start

Para início rápido, veja **[QUICK_START.md](QUICK_START.md)**

### 1. Criar e ativar ambiente virtual

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# ou
venv\Scripts\activate.bat     # Windows CMD
```

### 2. Instalar dependências básicas

```bash
pip install -r requirements.txt
```

### 3. Instalar face-recognition (requer CMake)

```bash
# Após instalar CMake e Visual Studio Build Tools:
pip install dlib
pip install face-recognition==1.3.0

# OU instalar tudo de uma vez:
pip install -r requirements-optional.txt
```

**Nota**: Se você encontrar erros na instalação do `dlib`, certifique-se de que:
- CMake está no PATH (teste com `cmake --version`)
- Visual Studio Build Tools está instalado
- Terminal foi reiniciado após instalar CMake

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
API_KEY=your-secret-api-key-123
WEBHOOK_URL=https://seu-webhook-url.com/notify
```

## 🏃 Como Executar

```bash
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📚 Endpoints da API

### 1. **Treinar Rosto**
```http
POST /train
Headers:
  x-api-key: your-secret-api-key-123
  Content-Type: multipart/form-data
Body:
  file: [imagem]
  name: "João Silva"
  face_id: "joao_001" (opcional)
```

**Resposta:**
```json
{
  "success": true,
  "message": "Rosto de João Silva treinado com sucesso",
  "face_id": "joao_001"
}
```

### 2. **Iniciar Reconhecimento em Tempo Real**
```http
POST /recognize/start
Headers:
  x-api-key: your-secret-api-key-123
```

### 3. **Parar Reconhecimento**
```http
POST /recognize/stop
Headers:
  x-api-key: your-secret-api-key-123
```

### 4. **Status do Sistema**
```http
GET /status
```

**Resposta:**
```json
{
  "camera_active": true,
  "trained_faces_count": 5,
  "last_recognition": "2025-01-31T18:00:00",
  "uptime_seconds": 3600.5
}
```

### 5. **Reconhecer Face em Imagem**
```http
POST /recognize/image
Headers:
  x-api-key: your-secret-api-key-123
  Content-Type: multipart/form-data
Body:
  file: [imagem]
```

## 🔗 Integração com Lovable (Frontend)

### Exemplo React/JavaScript

```javascript
// Treinar rosto
async function trainFace(file, name) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("name", name);

  const response = await fetch("http://localhost:8000/train", {
    method: "POST",
    headers: {
      "x-api-key": "your-secret-api-key-123"
    },
    body: formData
  });

  return await response.json();
}

// Iniciar reconhecimento
async function startRecognition() {
  const response = await fetch("http://localhost:8000/recognize/start", {
    method: "POST",
    headers: {
      "x-api-key": "your-secret-api-key-123"
    }
  });

  return await response.json();
}

// Verificar status
async function getStatus() {
  const response = await fetch("http://localhost:8000/status");
  return await response.json();
}
```

## 🏗️ Estrutura do Projeto

```
face-recognition-api/
│
├── app/
│   ├── main.py              # API principal (FastAPI)
│   ├── routes/
│   │   ├── train.py         # Endpoint /train
│   │   ├── recognize.py     # Endpoint /recognize
│   │   ├── status.py        # Endpoint /status
│   │   └── alert.py         # Endpoint /alert
│   ├── services/
│   │   ├── face_service.py  # Lógica de reconhecimento/treinamento
│   │   ├── camera_service.py# Loop de câmera em thread
│   │   └── alert_service.py # Notificações webhook
│   ├── models.py            # Modelos de dados (Pydantic)
│   ├── database.py          # Persistência (SQLite)
│   └── utils.py             # Utilitários
│
├── data/
│   ├── trained_faces/       # Fotos de treinamento (opcional)
│   └── face_recognition.db  # Banco de dados SQLite
│
├── requirements.txt         # Dependências básicas
├── requirements-optional.txt# face-recognition (requer CMake)
├── .env                     # Variáveis de ambiente
└── README.md
```

## 🔒 Segurança

- API protegida com API Key via header `x-api-key`
- Configure uma API key segura no arquivo `.env`
- Em produção, configure CORS adequadamente

## 🐛 Troubleshooting

### Erro ao instalar dlib:
- Verifique se CMake está instalado: `cmake --version`
- Verifique se Visual Studio Build Tools está instalado
- Reinicie o terminal após instalar CMake

### Câmera não funciona:
- Verifique se a câmera não está sendo usada por outro aplicativo
- Teste diferentes índices de câmera (0, 1, 2, etc.)

### Face-recognition não reconhece:
- Certifique-se de que as imagens de treinamento têm boa qualidade
- Verifique iluminação adequada
- Tente ajustar a tolerância no código

## 📝 Licença

Este projeto é open-source e está disponível para uso livre.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.
