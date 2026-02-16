@echo off
setlocal
title Painel de Producao - Emulsao
echo ============================================
echo    INICIANDO DASHBOARD DE PRODUCAO
echo ============================================
echo.

:: 1. Verifica se o ambiente virtual existe antes de tentar abrir
if not exist "venv\Scripts\activate.bat" (
    echo [X] ERRO: Pasta 'venv' nao encontrada. 
    echo Rode o 'instalacao.bat' primeiro!
    pause
    exit /b
)

:: 2. Ativa o ambiente
call venv\Scripts\activate.bat

:: 3. Roda o Streamlit com o FIX de 2026 para Python 3.13
:: O parametro --server.fileWatcherType none evita que o app feche sozinho no erro de Threads
echo [+] Otimizando sistema para Python 3.13...
streamlit run app.py --server.fileWatcherType none

echo.
echo [!] O servidor foi encerrado ou falhou. Verifique as mensagens acima.
echo.
pause