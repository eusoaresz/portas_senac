# grafo.py - lê o arestas.txt e monta a lista de adjacência do prédio.
# cada porta é um nó e cada linha do arquivo é uma aresta com o peso em passos.
import os

# o caminho do arquivo é montado a partir da pasta deste .py, para rodar de qualquer lugar
arq_arestas = os.path.join(os.path.dirname(__file__), "arestas.txt")


def carregar_grafo(caminho=arq_arestas):
    # grafo = dicionário onde a chave é a porta e o valor é a lista de (vizinho, peso)
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
            # anda-se nos dois sentidos, então cada linha vira duas entradas
            grafo[a].append((b, peso))
            grafo[b].append((a, peso))
    return grafo


def contar_arestas(grafo):
    total = 0
    for porta in grafo:
        total += len(grafo[porta])
    # cada aresta foi contada duas vezes (ida e volta)
    return total // 2


if __name__ == "__main__":
    from buscas import bfs

    # conferência do grafo: compara portas e arestas com o desenho
    grafo = carregar_grafo()
    print("Portas:", len(grafo))
    print("Arestas:", contar_arestas(grafo))

    # a BFS a partir do LABTEC tem que chegar em todas as portas, senão falta aresta no arquivo
    nao_alcancadas = []
    for porta in grafo:
        caminho, custo, visitados = bfs(grafo, "LABTEC", porta)
        if len(caminho) == 0:
            nao_alcancadas.append(porta)

    if len(nao_alcancadas) == 0:
        print("A BFS a partir do LABTEC alcança todas as portas.")
    else:
        print("Portas não alcançadas a partir do LABTEC:", ", ".join(nao_alcancadas))