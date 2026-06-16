@echo off
setlocal EnableExtensions

cd /d "%~dp0"

echo.
echo [INFO] Iniciando instalacao no Windows.
echo.

where python >nul 2>&1
if errorlevel 1 goto :python_missing

python --version >nul 2>&1
if errorlevel 1 goto :python_missing

echo [INFO] Python encontrado.

if not exist venv (
    echo [INFO] Criando ambiente virtual em venv...
    python -m venv venv
    if errorlevel 1 goto :venv_error
) else (
    echo [INFO] Ambiente virtual venv ja existe.
)

echo [INFO] Ativando o ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 goto :activate_error

echo [INFO] Instalando dependencias do projeto...
python -m pip install -r requirements.txt
if errorlevel 1 goto :pip_error

echo [INFO] Instalando o Chromium do Playwright...
python -m playwright install chromium
if errorlevel 1 goto :playwright_error

echo.
echo [INFO] Instalacao concluida com sucesso.
echo.
pause
exit /b 0

:python_missing
echo.
echo [ERRO] Python nao foi encontrado no PATH.
echo [ERRO] Instale o Python 3 a partir de https://www.python.org/downloads/
echo [ERRO] e marque a opcao para adicionar o Python ao PATH durante a instalacao.
echo.
pause
exit /b 1

:venv_error
echo.
echo [ERRO] Nao foi possivel criar o ambiente virtual.
echo [ERRO] Verifique se sua instalacao do Python inclui o modulo venv.
echo.
pause
exit /b 1

:activate_error
echo.
echo [ERRO] Nao foi possivel ativar o ambiente virtual.
echo.
pause
exit /b 1

:pip_error
echo.
echo [ERRO] Falha ao instalar as dependencias do requirements.txt.
echo.
pause
exit /b 1

:playwright_error
echo.
echo [ERRO] Falha ao instalar o Chromium do Playwright.
echo.
pause
exit /b 1
