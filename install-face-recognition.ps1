# Script de instalação do face-recognition no Windows (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Instalação do face-recognition no Windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se CMake está instalado
Write-Host "Verificando CMake..." -ForegroundColor Yellow
try {
    $cmakeVersion = cmake --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "CMake encontrado!" -ForegroundColor Green
        Write-Host $cmakeVersion -ForegroundColor Gray
    } else {
        throw "CMake não encontrado"
    }
} catch {
    Write-Host ""
    Write-Host "[ERRO] CMake não encontrado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor, instale o CMake:" -ForegroundColor Yellow
    Write-Host "1. Acesse: https://cmake.org/download/" -ForegroundColor White
    Write-Host "2. Baixe e instale o CMake" -ForegroundColor White
    Write-Host "3. IMPORTANTE: Marque 'Add CMake to system PATH' durante instalação" -ForegroundColor White
    Write-Host "4. Reinicie o terminal e execute este script novamente" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Instalando dlib..." -ForegroundColor Yellow
python -m pip install dlib

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERRO] Falha ao instalar dlib." -ForegroundColor Red
    Write-Host "Verifique se Visual Studio Build Tools está instalado." -ForegroundColor Yellow
    Write-Host "Download: https://visualstudio.microsoft.com/downloads/" -ForegroundColor White
    exit 1
}

Write-Host "Instalando face-recognition..." -ForegroundColor Yellow
python -m pip install face-recognition==1.3.0

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[SUCESSO] face-recognition instalado com sucesso!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[ERRO] Falha na instalação do face-recognition." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Verificando instalação..." -ForegroundColor Yellow
python -c "import face_recognition; print('face_recognition OK')"

if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCESSO] Tudo pronto!" -ForegroundColor Green
} else {
    Write-Host "[AVISO] Instalação pode estar incompleta." -ForegroundColor Yellow
}
