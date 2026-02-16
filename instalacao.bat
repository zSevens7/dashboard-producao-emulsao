@echo off
setlocal EnableDelayedExpansion
title Instalador Inteligente - Painel de Producao

echo ======================================================
echo    INSTALADOR AUTOMATICO - DASHBOARD DE ENGENHARIA
echo ======================================================
echo.

:: 1. Verificar se o Python e REALMENTE funcional
:: Tentamos rodar um comando simples. Se falhar, o Python nao esta instalado de fato.
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python nao funcional ou nao encontrado.
    echo [!] Tentando instalacao automatica via Winget...
    
    :: Tenta instalar o Python 3.13 oficial
    winget install Python.Python.3.13 --silent --accept-package-agreements --accept-source-agreements
    
    if %errorlevel% neq 0 (
        echo [X] Falha na instalacao automatica. 
        echo [!] Por favor, instale manualmente em: https://www.python.org/downloads/
        echo [!] Marque a opcao "Add Python to PATH" durante a instalacao.
        pause
        exit /b
    )
    echo [OK] Python instalado! REINICIE este arquivo para continuar.
    pause
    exit /b
)

echo [OK] Python detectado e funcional.

:: 2. Criar Ambiente Virtual (VENV)
if not exist "venv" (
    echo [+] Criando ambiente virtual de seguranca...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [X] Erro ao criar VENV. Tentando comando alternativo 'py'...
        py -m venv venv
        if %errorlevel% neq 0 (
            echo [X] Erro critico ao criar ambiente virtual.
            pause
            exit /b
        )
    )
)

:: 3. Ativar e instalar dependencias
echo [+] Ativando ambiente e atualizando bibliotecas...
call venv\Scripts\activate.bat

:: Garante que o PIP esteja atualizado dentro do VENV
python -m pip install --upgrade pip

if not exist "requirements.txt" (
    echo [X] Erro: Arquivo 'requirements.txt' nao encontrado!
    pause
    exit /b
)

echo [+] Instalando dependencias (isso pode demorar na primeira vez)...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [X] Houve um erro na instalacao das bibliotecas.
    pause
    exit /b
)

echo.
echo ======================================================
echo    INSTALACAO FINALIZADA COM SUCESSO!
echo    Agora voce pode usar o 'executar.bat'
echo ======================================================
pause