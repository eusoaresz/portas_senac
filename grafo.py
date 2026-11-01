import os

arq_arestas = os.path.join(os.path.dirname(__file__), "arestas.txt")


def carregar_grafo(caminho=arq_arestas):
    grafo = {}
    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip() == "":
                continue
            partes = linha.split()
            a = partes[0]
            b = partes[1]
            peso = int(partes[2])
            if a not in grafo:
                grafo[a] = []
            if b not in grafo:
                grafo[b] = []
            grafo[a].append((b, peso))
            grafo[b].append((a, peso))
    return grafo


def contar_arestas(grafo):
    total = 0
    for porta in grafo:
        total += len(grafo[porta])
    return total // 2


if __name__ == "__main__":
    from buscas import bfs

    grafo = carregar_grafo()
    print("Portas:", len(grafo))
    print("Arestas:", contar_arestas(grafo))

    nao_alcancadas = []
    for porta in grafo:
        caminho, custo, visitados = bfs(grafo, "LABTEC", porta)
        if len(caminho) == 0:
            nao_alcancadas.append(porta)

    if len(nao_alcancadas) == 0:
        print("A BFS a partir do LABTEC alcança todas as portas.")
    else:
        print("Portas não alcançadas a partir do LABTEC:", ", ".join(nao_alcancadas))
