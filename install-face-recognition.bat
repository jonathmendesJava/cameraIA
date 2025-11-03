@echo off
echo ========================================
echo Instalacao do face-recognition no Windows
echo ========================================
echo.
echo Este script vai tentar instalar face-recognition.
echo Se falhar, voce precisara instalar CMake primeiro.
echo.
echo Verificando CMake...
cmake --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] CMake nao encontrado!
    echo.
    echo Por favor, instale o CMake:
    echo 1. Acesse: https://cmake.org/download/
    echo 2. Baixe e instale o CMake
    echo 3. IMPORTANTE: Marque "Add CMake to system PATH" durante instalacao
    echo 4. Reinicie o terminal e execute este script novamente
    echo.
    pause
    exit /b 1
)

echo CMake encontrado! Continuando instalacao...
echo.

call venv\Scripts\activate.bat
pip install dlib
pip install face-recognition==1.3.0

if %errorlevel% equ 0 (
    echo.
    echo [SUCESSO] face-recognition instalado com sucesso!
) else (
    echo.
    echo [ERRO] Falha na instalacao.
    echo Verifique se Visual Studio Build Tools esta instalado.
)

pause
