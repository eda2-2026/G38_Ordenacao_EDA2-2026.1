from fastapi import FastAPI, HTTPException, Query, Path
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

# Estado em memoria: para que randomizar e ordenar nao afetem o JSON permanentemente
dados_em_memoria = carregar_dados()

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend ainda não construído."}

@app.get("/api/jogadores")
def get_jogadores():
    """Retorna a lista atual em memória."""
    return dados_em_memoria

@app.post("/api/jogadores")
def add_jogador(jogador: Jogador):
    """Adiciona um novo jogador na memoria e no JSON."""
    global dados_em_memoria
    
    if not jogador.nome.strip():
        raise HTTPException(status_code=400, detail="Adicione um nome!")
    
    for d in dados_em_memoria:
        if d['nome'].lower().strip() == jogador.nome.lower().strip():
            raise HTTPException(status_code=400, detail="Jogador já existe com este nome.")
            
    novo_jogador = jogador.dict()
    dados_em_memoria.append(novo_jogador)
    
    # Salva no arquivo JSON (persistencia permanente)
    salvar_dados(carregar_dados() + [novo_jogador]) 
    # Melhor reconstruir do JSON para garantir consistência ou só salvar a lista atual
    # Como a lista atual pode estar randomizada, vamos apenas adicionar ao JSON original.
    json_atual = carregar_dados()
    json_atual.append(novo_jogador)
    salvar_dados(json_atual)
    
    return {"message": "Jogador adicionado com sucesso!", "jogador": novo_jogador}

@app.post("/api/jogadores/randomizar")
def randomizar_jogadores():
    """Embaralha a lista em memória (NÃO afeta o JSON)."""
    global dados_em_memoria
    random.shuffle(dados_em_memoria)
    return {"message": "Lista randomizada na memória!", "jogadores": dados_em_memoria}

@app.get("/api/jogadores/ordenar")
def get_jogadores_ordenados(
    criterio: str = Query(..., description="Chave para ordenação (ex: nome, posicao, pago)")
):
    """Ordena a lista usando os 3 algoritmos para comparar tempo (NÃO afeta o JSON permanentemente)."""
    global dados_em_memoria
    
    if not dados_em_memoria:
        return {"jogadores": [], "tempos": {"bubble": 0.0, "merge": 0.0, "quick": 0.0}}
        
    if criterio not in dados_em_memoria[0]:
        raise HTTPException(status_code=400, detail=f"Critério '{criterio}' inválido.")
        
    # Cópias independentes para cada algoritmo (garante que todos ordenem a mesma lista embaralhada)
    lista_bubble = dados_em_memoria[:]
    lista_merge = dados_em_memoria[:]
    lista_quick = dados_em_memoria[:]
    
    tempos = {}
    
    # 1. Bubble Sort
    start_time = time.perf_counter()
    bubble_sort(lista_bubble, criterio)
    tempos['bubble'] = (time.perf_counter() - start_time) * 1000
    
    # 2. Merge Sort
    start_time = time.perf_counter()
    merge_sort(lista_merge, criterio)
    tempos['merge'] = (time.perf_counter() - start_time) * 1000
    
    # 3. Quick Sort
    start_time = time.perf_counter()
    dados_ordenados = quick_sort(lista_quick, criterio)
    tempos['quick'] = (time.perf_counter() - start_time) * 1000
    
    # Atualiza a memória com o resultado ordenado
    dados_em_memoria = dados_ordenados
    
    return {"jogadores": dados_em_memoria, "tempos": tempos}

@app.get("/api/jogadores/buscar")
def buscar_jogador(nome: str = Query(..., description="Nome do jogador a buscar")):
    """Busca um jogador pelo nome na lista em memoria."""
    # Busca sequencial simples
    resultados = [j for j in dados_em_memoria if nome.lower() in j['nome'].lower()]
    return resultados

@app.put("/api/jogadores/{nome}/pagamento")
def alterar_pagamento(nome: str = Path(..., description="Nome do jogador")):
    """Altera o status de pagamento do jogador na memoria e no JSON."""
    global dados_em_memoria
    
    jogador_memoria = next((j for j in dados_em_memoria if j['nome'].lower() == nome.lower()), None)
    if not jogador_memoria:
        raise HTTPException(status_code=404, detail="Jogador não encontrado.")
        
    # Altera na memoria
    jogador_memoria['pago'] = not jogador_memoria['pago']
    
    # Altera no JSON
    json_atual = carregar_dados()
    jogador_json = next((j for j in json_atual if j['nome'].lower() == nome.lower()), None)
    if jogador_json:
        jogador_json['pago'] = jogador_memoria['pago']
        salvar_dados(json_atual)
        
    return {"message": f"Status de pagamento de {jogador_memoria['nome']} atualizado!", "jogador": jogador_memoria}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
