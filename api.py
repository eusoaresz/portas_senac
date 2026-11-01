from fastapi import FastAPI, HTTPException

from buscas import algoritmos
from grafo import carregar_grafo

app = FastAPI(title="Rotas do Prédio")

grafo = carregar_grafo()


def checar_porta(porta):
    porta = porta.strip().upper()
    if porta not in grafo:
        raise HTTPException(404, "Porta não encontrada: " + porta)
    return porta


def rodar_busca(algoritmo, origem, destino):
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
    return sorted(grafo)


@app.get("/vizinhos/{porta}")
def vizinhos(porta: str):
    porta = checar_porta(porta)
    lista = []
    for vizinho, peso in grafo[porta]:
        lista.append({"porta": vizinho, "peso": peso})
    return lista


@app.get("/rota")
def rota(origem: str, destino: str, algoritmo: str):
    origem = checar_porta(origem)
    destino = checar_porta(destino)
    algoritmo = algoritmo.strip().lower()
    if algoritmo not in algoritmos:
        raise HTTPException(400, "Algoritmo inválido: use " + ", ".join(algoritmos.keys()))
    return rodar_busca(algoritmo, origem, destino)


@app.get("/comparar")
def comparar(origem: str, destino: str):
    origem = checar_porta(origem)
    destino = checar_porta(destino)
    resultados = []
    for nome in algoritmos:
        resultados.append(rodar_busca(nome, origem, destino))
    return {"origem": origem, "destino": destino, "resultados": resultados}
