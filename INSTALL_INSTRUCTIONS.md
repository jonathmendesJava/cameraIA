# 📦 Instruções de Instalação do face-recognition

## ⚠️ IMPORTANTE

O `face-recognition` requer ferramentas de compilação no Windows. Siga estes passos:

## Opção 1: Instalação Automática (PowerShell)

Execute o script que criamos:

```powershell
.\install-face-recognition.ps1
```

O script irá:
- Verificar se CMake está instalado
- Instalar dlib
- Instalar face-recognition

## Opção 2: Instalação Manual

### Passo 1: Instalar CMake

1. Acesse: https://cmake.org/download/
2. Baixe o instalador para Windows
3. **IMPORTANTE**: Durante a instalação, marque a opção:
   - ✅ **"Add CMake to system PATH"**
4. Reinicie o terminal após a instalação

### Passo 2: Instalar Visual Studio Build Tools

1. Acesse: https://visualstudio.microsoft.com/downloads/
2. Baixe "Build Tools for Visual Studio"
3. Execute o instalador
4. Selecione o workload:
   - ✅ **"Desktop development with C++"**
5. Instale

### Passo 3: Instalar face-recognition

No terminal (após reiniciar):

```powershell
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar dlib
pip install dlib

# Instalar face-recognition
pip install face-recognition==1.3.0
```

### Passo 4: Verificar Instalação

```python
python -c "import face_recognition; print('✅ face-recognition instalado!')"
```

## ✅ Verificação

Se tudo estiver correto, ao iniciar a API você verá:

```
🚀 Face Recognition API iniciada!
✅ face-recognition disponível!
📊 Rostos treinados: 0
```

## ❌ Problemas Comuns

### "CMake não encontrado"
- Verifique se CMake está no PATH: `cmake --version`
- Reinicie o terminal após instalar CMake
- Adicione CMake manualmente ao PATH se necessário

### "Microsoft Visual C++ 14.0 or greater is required"
- Instale Visual Studio Build Tools
- Certifique-se de selecionar "Desktop development with C++"

### "Failed building wheel for dlib"
- Verifique se CMake está instalado e no PATH
- Verifique se Visual Studio Build Tools está instalado
- Tente instalar apenas: `pip install dlib` primeiro

## 🔄 Alternativas

Se você continuar tendo problemas, considere:

1. **Usar WSL2** (Windows Subsystem for Linux) - mais fácil instalar no Linux
2. **Usar Docker** - container pré-configurado
3. **Usar uma VM Linux** - Ubuntu/Debian facilitam a instalação

## 📞 Suporte

Se ainda tiver problemas, verifique:
- Versão do Python (recomendado: 3.11+)
- Versão do pip: `pip --version`
- Espaço em disco (compilação pode precisar de alguns GB)
