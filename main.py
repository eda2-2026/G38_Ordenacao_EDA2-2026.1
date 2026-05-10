from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os

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

@app.get("/api/jogadores/ordenar")
def get_jogadores_ordenados(
    criterio: str = Query(..., description="Chave para ordenação (ex: nome, posicao, pago)"),
    algoritmo: str = Query(..., description="Algoritmo de ordenação (bubble, merge, quick)")
):
    dados = carregar_dados()
    
    if not dados:
        return []
        
    if criterio not in dados[0]:
        raise HTTPException(status_code=400, detail=f"Critério '{criterio}' inválido.")
        
    if algoritmo == 'bubble':
        return bubble_sort(dados, criterio)
    elif algoritmo == 'merge':
        return merge_sort(dados, criterio)
    elif algoritmo == 'quick':
        return quick_sort(dados, criterio)
    else:
        raise HTTPException(status_code=400, detail=f"Algoritmo '{algoritmo}' não suportado.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
