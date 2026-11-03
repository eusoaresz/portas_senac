# buscas.py - BFS, DFS e busca gulosa no grafo do prédio.
# as três funções recebem (grafo, origem, destino) e devolvem (caminho, custo, visitados).
# visitados = portas examinadas até achar o destino (o destino conta).
import sys
from collections import deque

from grafo import carregar_grafo


def reconstruir(anterior, destino):
    # parte do destino e volta pelos antecessores até a origem, depois inverte a lista
    if destino not in anterior:
        return []
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = anterior[atual]
    return caminho[::-1]


def peso_da_aresta(grafo, a, b):
    # devolve o peso da aresta entre duas portas, ou None se não houver aresta
    for vizinho, peso in grafo[a]:
        if vizinho == b:
            return peso
    return None

def custo_do_caminho(grafo, caminho):
    # soma os pesos das arestas entre cada par de portas seguidas do caminho
    custo = 0
    for i in range(len(caminho) - 1):
        custo += peso_da_aresta(grafo, caminho[i], caminho[i + 1])
    return custo


def bfs(grafo, origem, destino):
    # BFS usa fila, então explora por camadas de portas e ignora o peso das arestas
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
    # parte recursiva da DFS: entra no primeiro vizinho novo e só volta se não achar o destino
    if atual == destino:
        return True
    for vizinho, peso in grafo[atual]:
        if vizinho not in anterior:
            anterior[vizinho] = atual
            if visitar(grafo, vizinho, destino, anterior):
                return True
    return False


def dfs(grafo, origem, destino):
    # o caminho depende da ordem dos vizinhos, que é a ordem das linhas do arestas.txt
    anterior = {origem: None}
    visitar(grafo, origem, destino, anterior)
    caminho = reconstruir(anterior, destino)
    custo = custo_do_caminho(grafo, caminho)
    # na DFS toda porta descoberta é visitada na hora, então visitados = len(anterior)
    return caminho, custo, len(anterior)


def gulosa(grafo, origem, destino):
    # gulosa: em cada porta vai para o vizinho ainda não visitado com a menor aresta
    # ela não compara com outros caminhos, por isso não garante o menor custo
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
            # beco sem saída: recua uma porta para não ficar presa
            caminho.pop()
        else:
            visitados.append(melhor)
            caminho.append(melhor)
    return [], 0, len(visitados)


# usado pela API e pelo modo de linha de comando; o Dijkstra entra aqui depois
algoritmos = {"bfs": bfs, "dfs": dfs, "gulosa": gulosa}


if __name__ == "__main__":
    # uso: python buscas.py origem destino
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