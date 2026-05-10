@echo off
echo =======================================================
echo    Iniciando Organizador de Pelada (EDA2)
echo =======================================================

:: Verifica se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado! Instale o Python 3 antes de continuar.
    pause
    exit /b
)

:: Cria ambiente virtual se nao existir
if not exist "venv\" (
    echo [INFO] Criando ambiente virtual...
    python -m venv venv
)

:: Ativa e instala dependencias
echo [INFO] Instalando/Verificando dependencias...
call venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1

echo.
echo =======================================================
echo    Servidor Iniciado! 
echo    Pressione CTRL+C nesta janela para fechar.
echo.
echo    Acesse no seu navegador: http://127.0.0.1:8000
echo =======================================================
echo.

:: Abre o navegador padrao
start http://127.0.0.1:8000

:: Roda o servidor
python -m uvicorn main:app --host 127.0.0.1 --port 8000
