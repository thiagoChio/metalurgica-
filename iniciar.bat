@echo off
chcp 65001 >nul
title Correa Metalurgica - site local
cd /d "%~dp0"

echo.
echo ===============================================
echo   CORREA METALURGICA - servidor local
echo ===============================================
echo.

REM --- procura o Python instalado -------------------------------------
where py >nul 2>nul
if %errorlevel%==0 (set PY=py) else (
  where python >nul 2>nul
  if %errorlevel%==0 (set PY=python) else (
    echo [ERRO] Python nao encontrado.
    echo Instale em https://www.python.org/downloads/
    echo IMPORTANTE: marque "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
  )
)

REM --- cria o ambiente na primeira execucao ---------------------------
if not exist ".venv\Scripts\python.exe" (
  echo Primeira execucao: preparando o ambiente. Leva 1 ou 2 minutos...
  echo.
  %PY% -m venv .venv
  if errorlevel 1 goto erro
  call .venv\Scripts\python.exe -m pip install --upgrade pip --quiet
  call .venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
  if errorlevel 1 goto erro
  echo Ambiente pronto.
  echo.
)

echo Abrindo http://127.0.0.1:8000 no navegador...
echo Para encerrar o servidor, feche esta janela ou pressione Ctrl+C.
echo.
start "" http://127.0.0.1:8000
call .venv\Scripts\python.exe run.py
goto fim

:erro
echo.
echo [ERRO] Falha ao preparar o ambiente. Veja a mensagem acima.
pause
exit /b 1

:fim
pause
