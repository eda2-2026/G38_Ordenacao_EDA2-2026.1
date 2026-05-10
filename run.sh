#!/bin/bash

echo "======================================================="
echo "   Iniciando Organizador de Pelada (EDA2)"
echo "======================================================="

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null
then
    echo "[ERRO] Python 3 nao encontrado! Instale o Python 3 antes de continuar."
    exit
fi

# Cria ambiente virtual se nao existir
if [ ! -d "venv" ]; then
    echo "[INFO] Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativa e instala dependencias
echo "[INFO] Instalando/Verificando dependencias..."
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

echo ""
echo "======================================================="
echo "   Servidor Iniciado!"
echo "   Pressione CTRL+C nesta janela para fechar."
echo ""
echo "   Acesse no seu navegador: http://127.0.0.1:8000"
echo "======================================================="
echo ""

# Roda o servidor
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
