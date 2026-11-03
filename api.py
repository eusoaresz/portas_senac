# api.py - API FastAPI com as rotas do prédio.
# para rodar: uvicorn api:app --reload  e abrir http://127.0.0.1:8000/docs
from fastapi import FastAPI, HTTPException

from buscas import algoritmos
from grafo import carregar_grafo

app = FastAPI(title="Rotas do Prédio")

# o grafo é carregado uma vez só, quando a API inicia
grafo = carregar_grafo()


def checar_porta(porta):
    # aceita minúsculas e espaços; porta que não existe devolve 404
    porta = porta.strip().upper()
    if porta not in grafo:
        raise HTTPException(404, "Porta não encontrada: " + porta)
    return porta


def rodar_busca(algoritmo, origem, destino):
    # roda um algoritmo do dicionário algoritmos e devolve o resultado
    busca = algoritmos[algoritmo]
    caminho, custo, visitados = busca(grafo, origem, destino)
    return {
        "algoritmo": algoritmo,
        "caminho": caminho,
        "custo": custo,
        "unidade": "passos",
        "visitados": visitados,
    }


@app.get("/portas")
def portas():
    # lista todas as portas do prédio
    return sorted(grafo)


@app.get("/vizinhos/{porta}")
def vizinhos(porta: str):
    # vizinhos de uma porta, cada um com o peso da aresta
    porta = checar_porta(porta)
    lista = []
    for vizinho, peso in grafo[porta]:
        lista.append({"porta": vizinho, "peso": peso})
    return lista


@app.get("/rota")
def rota(origem: str, destino: str, algoritmo: str):
    # caminho, custo e visitados de um algoritmo; algoritmo desconhecido devolve 400
    origem = checar_porta(origem)
    destino = checar_porta(destino)
    algoritmo = algoritmo.strip().lower()
    if algoritmo not in algoritmos:
        raise HTTPException(400, "Algoritmo inválido: use " + ", ".join(algoritmos.keys()))
    return rodar_busca(algoritmo, origem, destino)


@app.get("/comparar")
def comparar(origem: str, destino: str):
    # roda todos os algoritmos do dicionário algoritmos para o mesmo par de portas
    origem = checar_porta(origem)
    destino = checar_porta(destino)
    resultados = []
    for nome in algoritmos:
        resultados.append(rodar_busca(nome, origem, destino))
    return {"origem": origem, "destino": destino, "resultados": resultados}
