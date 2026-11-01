import sys
from collections import deque

from grafo import carregar_grafo


def reconstruir(anterior, destino):
    if destino not in anterior:
        return []
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = anterior[atual]
    return caminho[::-1]


def peso_da_aresta(grafo, a, b):
    for vizinho, peso in grafo[a]:
        if vizinho == b:
            return peso


def custo_do_caminho(grafo, caminho):
    custo = 0
    for i in range(len(caminho) - 1):
        custo += peso_da_aresta(grafo, caminho[i], caminho[i + 1])
    return custo


def bfs(grafo, origem, destino):
    fila = deque([origem])
    anterior = {origem: None}
    visitados = 0
    while fila:
        atual = fila.popleft()
        visitados += 1
        if atual == destino:
            break
        for vizinho, peso in grafo[atual]:
            if vizinho not in anterior:
                anterior[vizinho] = atual
                fila.append(vizinho)
    caminho = reconstruir(anterior, destino)
    custo = custo_do_caminho(grafo, caminho)
    return caminho, custo, visitados


def visitar(grafo, atual, destino, anterior):
    if atual == destino:
        return True
    for vizinho, peso in grafo[atual]:
        if vizinho not in anterior:
            anterior[vizinho] = atual
            if visitar(grafo, vizinho, destino, anterior):
                return True
    return False


def dfs(grafo, origem, destino):
    anterior = {origem: None}
    visitar(grafo, origem, destino, anterior)
    caminho = reconstruir(anterior, destino)
    custo = custo_do_caminho(grafo, caminho)
    return caminho, custo, len(anterior)


def gulosa(grafo, origem, destino):
    caminho = [origem]
    visitados = [origem]
    while len(caminho) > 0:
        atual = caminho[-1]
        if atual == destino:
            custo = custo_do_caminho(grafo, caminho)
            return caminho, custo, len(visitados)

        melhor = None
        menor_peso = None
        for vizinho, peso in grafo[atual]:
            if vizinho in visitados:
                continue
            if menor_peso is None or peso < menor_peso:
                menor_peso = peso
                melhor = vizinho

        if melhor is None:
            caminho.pop()
        else:
            visitados.append(melhor)
            caminho.append(melhor)
    return [], 0, len(visitados)


algoritmos = {"bfs": bfs, "dfs": dfs, "gulosa": gulosa}


if __name__ == "__main__":
    origem = "LABTEC"
    destino = "SAIDA_P2"
    if len(sys.argv) > 2:
        origem = sys.argv[1].upper()
        destino = sys.argv[2].upper()

    grafo = carregar_grafo()
    if origem not in grafo or destino not in grafo:
        sys.exit("Porta não encontrada. Use os nomes do arestas.txt.")

    print(origem, "->", destino)
    print()
    print(f"{'algoritmo':<10}{'passos':>8}{'portas':>8}{'visitados':>12}")
    for nome in algoritmos:
        busca = algoritmos[nome]
        caminho, custo, visitados = busca(grafo, origem, destino)
        print(f"{nome:<10}{custo:>8}{len(caminho):>8}{visitados:>12}")
        print("   " + " -> ".join(caminho))
