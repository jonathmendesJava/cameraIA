# 🔧 Solução: Problemas ao Ativar Ambiente Virtual no Windows

## 🐛 Problemas Comuns

### Problema 1: Erro "execution of scripts is disabled"

**Erro:**
```
.\venv\Scripts\Activate.ps1 : Não é possível carregar o arquivo ... porque a execução de scripts foi desabilitada neste sistema.
```

**Solução:**

Abra o PowerShell **como Administrador** e execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois, tente novamente:
```powershell
.\venv\Scripts\Activate.ps1
```

### Problema 2: Script executa mas nada acontece

**Causa:** O ambiente pode estar ativado, mas não está visível.

**Verificação:**
```powershell
# Verificar se está ativado
python --version
# Deve mostrar o Python do venv

# Ou verificar o caminho
python -c "import sys; print(sys.executable)"
# Deve mostrar: ...\venv\Scripts\python.exe
```

### Problema 3: Não consigo ativar de jeito nenhum

**Solução Alternativa 1: Usar CMD (Prompt de Comando)**

Em vez do PowerShell, use o **Prompt de Comando (CMD)**:

```cmd
venv\Scripts\activate.bat
```

**Solução Alternativa 2: Usar o Python direto**

Você pode usar o Python do ambiente virtual sem ativar:

```powershell
# Em vez de: python
.\venv\Scripts\python.exe -m pip install ...

# Em vez de: pip
.\venv\Scripts\pip.exe install ...
```

**Solução Alternativa 3: Executar o script com bypass**

```powershell
powershell -ExecutionPolicy Bypass -File .\venv\Scripts\Activate.ps1
```

## ✅ Verificação Passo a Passo

### 1. Verificar se o ambiente virtual existe

```powershell
Test-Path .\venv\Scripts\Activate.ps1
# Deve retornar: True
```

### 2. Verificar política de execução

```powershell
Get-ExecutionPolicy
# Deve ser: RemoteSigned, Unrestricted ou Bypass
```

### 3. Tentar ativar

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Verificar se está ativo

```powershell
# Verificar variável de ambiente
$env:VIRTUAL_ENV
# Deve mostrar o caminho do venv

# Verificar prompt
# O prompt deve mostrar (venv) no início
```

## 🎯 Soluções por Situação

### Se você está no PowerShell normal:

```powershell
# Método 1: Mudar política
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1

# Método 2: Executar com bypass
powershell -ExecutionPolicy Bypass -File .\venv\Scripts\Activate.ps1

# Método 3: Usar caminho direto
.\venv\Scripts\python.exe -m pip install ...
```

### Se você está no PowerShell ISE:

O ISE pode ter problemas. Use o PowerShell normal ou CMD.

### Se você está no CMD:

```cmd
venv\Scripts\activate.bat
```

### Se você está no Git Bash:

```bash
source venv/Scripts/activate
```

## 🔍 Diagnóstico Avançado

### Verificar estrutura do venv

```powershell
# Listar arquivos do Scripts
Get-ChildItem .\venv\Scripts\

# Verificar se python.exe existe
Test-Path .\venv\Scripts\python.exe
```

### Verificar conteúdo do Activate.ps1

```powershell
# Ver primeiras linhas
Get-Content .\venv\Scripts\Activate.ps1 -Head 20
```

### Recriar ambiente virtual

Se nada funcionar, recrie o ambiente:

```powershell
# Remover o venv antigo
Remove-Item -Recurse -Force venv

# Criar novo
python -m venv venv

# Tentar ativar
.\venv\Scripts\Activate.ps1
```

## 📝 Comandos Úteis

### Ativar manualmente (sem script)

Você pode ativar manualmente definindo as variáveis:

```powershell
$env:VIRTUAL_ENV = (Resolve-Path .\venv).Path
$env:PATH = "$env:VIRTUAL_ENV\Scripts;$env:PATH"
```

### Usar sempre o Python do venv

Crie um alias:

```powershell
# No PowerShell
Set-Alias venv-python ".\venv\Scripts\python.exe"
Set-Alias venv-pip ".\venv\Scripts\pip.exe"

# Usar
venv-python --version
venv-pip install fastapi
```

## 🚀 Solução Recomendada

**Para a maioria dos casos, use CMD em vez de PowerShell:**

1. Abra o **Prompt de Comando (CMD)**
2. Navegue até o diretório do projeto:
   ```cmd
   cd C:\Users\jonat\Desktop\film.ai
   ```
3. Ative o ambiente:
   ```cmd
   venv\Scripts\activate.bat
   ```
4. Você verá `(venv)` no início do prompt
5. Use normalmente:
   ```cmd
   pip install dlib
   python -m uvicorn app.main:app --reload
   ```

## 📚 Referências

- [Documentação oficial do venv](https://docs.python.org/3/library/venv.html)
- [PowerShell Execution Policies](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)

---

**Dica Final**: Se você tiver muitos problemas, simplesmente use **CMD** (Prompt de Comando) em vez de PowerShell. É mais simples e funciona perfeitamente!
