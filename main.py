from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os
import time
import random

from dados import carregar_dados, salvar_dados
from ordenacao import bubble_sort, merge_sort, quick_sort

app = FastAPI(title="Organizador de Pelada API")

class Jogador(BaseModel):
    nome: str
    posicao: str
    pago: bool

# Configura as rotas para servir os arquivos estaticos do frontend
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    # Rota raiz serve o index.html principal
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend ainda não construído. Crie static/index.html"}

@app.get("/api/jogadores")
def get_jogadores():
    return carregar_dados()

@app.post("/api/jogadores")
def add_jogador(jogador: Jogador):
    dados = carregar_dados()
    
    for d in dados:
        if d['nome'].lower() == jogador.nome.lower():
            raise HTTPException(status_code=400, detail="Jogador já existe com este nome.")
            
    novo_jogador = jogador.dict()
    dados.append(novo_jogador)
    salvar_dados(dados)
    
    return {"message": "Jogador adicionado com sucesso!", "jogador": novo_jogador}

@app.post("/api/jogadores/randomizar")
def randomizar_jogadores():
    dados = carregar_dados()
    random.shuffle(dados)
    salvar_dados(dados)
    return {"message": "Lista randomizada com sucesso!", "jogadores": dados}

@app.get("/api/jogadores/ordenar")
def get_jogadores_ordenados(
    criterio: str = Query(..., description="Chave para ordenação (ex: nome, posicao, pago)"),
    algoritmo: str = Query(..., description="Algoritmo de ordenação (bubble, merge, quick)")
):
    dados = carregar_dados()
    
    if not dados:
        return {"jogadores": [], "tempo_ms": 0.0}
        
    if criterio not in dados[0]:
        raise HTTPException(status_code=400, detail=f"Critério '{criterio}' inválido.")
        
    start_time = time.perf_counter()
    
    if algoritmo == 'bubble':
        resultado = bubble_sort(dados, criterio)
    elif algoritmo == 'merge':
        resultado = merge_sort(dados, criterio)
    elif algoritmo == 'quick':
        resultado = quick_sort(dados, criterio)
    else:
        raise HTTPException(status_code=400, detail=f"Algoritmo '{algoritmo}' não suportado.")
        
    end_time = time.perf_counter()
    tempo_ms = (end_time - start_time) * 1000
    
    return {"jogadores": resultado, "tempo_ms": tempo_ms}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
