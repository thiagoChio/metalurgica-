@echo off
chcp 65001 >nul
title Correa Metalurgica - MODO APRESENTACAO
cd /d "%~dp0"

REM ==================================================================
REM  MODO APRESENTACAO
REM  Igual ao iniciar.bat, mas sem os lembretes de obra na tela.
REM  Use este quando for mostrar o site para o cliente.
REM ==================================================================
set SITE_DEBUG=false

echo.
echo ===============================================
echo   CORREA METALURGICA - MODO APRESENTACAO
echo   (sem lembretes de obra na tela)
echo ===============================================
echo.

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
echo Para encerrar, feche esta janela.
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
