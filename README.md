<<<<<<< HEAD
# Rotas do Prédio com Grafos

Trabalho de **Algoritmos e Estruturas de Dados II**, mapeando o prédio de nossa faculdade, UniSenac

O prédio é um grafo: cada **porta** é um nó e cada ligação entre duas portas vizinhas é uma **aresta**. O peso da aresta é a distância medida em passos só entre essas duas portas (não é a distância acumulada desde o LabTec). Uma API recebe duas portas e devolve o caminho encontrado por cada busca.

## Integrantes

Arthur Holz Leite
Roger Pereira Soares
Heitor Barbosa Hepp

## Unidade do peso

**Passos.** O ponto zero é o `LABTEC`.

O grafo tem **42 portas** e **59 arestas**.

## Como rodar

```sh
pip install -r requirements.txt
```

Conferir o grafo (número de portas e arestas, e se a BFS a partir do `LABTEC` alcança todas as portas):

```sh
python grafo.py
```

Comparar as buscas no terminal:

```sh
python buscas.py LABTEC SAIDA_P2
```

Subir a API:

```sh
uvicorn api:app --reload
```

Depois, abrir <http://127.0.0.1:8000/docs> para testar cada endpoint.

| Endpoint | Devolve |
|---|---|
| `GET /portas` | Todas as portas |
| `GET /vizinhos/{porta}` | Vizinhos e peso de cada aresta |
| `GET /rota?origem=&destino=&algoritmo=` | Caminho, custo e visitados (`bfs`, `dfs` ou `gulosa`) |
| `GET /comparar?origem=&destino=` | Os algoritmos lado a lado |

Porta inexistente devolve **404** com mensagem. Algoritmo inexistente devolve **400**.

## O que cada busca devolve

Todas as buscas têm a mesma assinatura: `funcao(grafo, origem, destino)` devolve `(caminho, custo, visitados)`.

- **caminho:** portas da origem ao destino.
- **custo:** soma dos pesos (passos) das arestas do caminho.
- **visitados:** portas examinadas até achar o destino, contando o próprio destino. Uma porta é examinada quando sai da fila (BFS) ou quando a busca entra nela (DFS e gulosa).

| Busca | Estrutura | Como decide |
|---|---|---|
| **BFS** | Fila | Explora por camadas de portas. Acha o caminho com menos portas e ignora o peso. |
| **DFS** | Pilha (recursão) | Vai fundo no primeiro vizinho da lista. O resultado depende da ordem das linhas do `arestas.txt`. |
| **Gulosa** | Escolha local | Em cada porta, vai para o vizinho ainda não visitado com a **menor aresta**. Não refaz a escolha. |

**Nenhuma das três garante o menor custo.** Para isso serve o Dijkstra, que ainda não está implementado.
A BFS conta portas, e todas as arestas valem o mesmo para ela. O caminho pelo pátio tem só duas arestas, mas uma delas é longa (25 passos). O Dijkstra soma os pesos. Por isso aceita passar por mais portas (6 contra 3) e chega com 12 passos a menos.

=======
# Mapeamento do prédio UniSenac

Atividade de Algoritmos e Estruturas de Dados II. O programa mapeia as portas do UniSenac a partir de um grafo e procura cada porta em arestas. Começa a partir do LabTech como ponto 0.
>>>>>>> 1a56eb594fd1164a63d3f7b321704cf23a06a8d6
