# Rotas do Prédio com Grafos

Trabalho de **Algoritmos e Estruturas de Dados II**, desenvolvido a partir do mapeamento do prédio da UniSenac.

O prédio é representado por um grafo: cada **porta** é um nó e cada ligação entre duas portas vizinhas é uma **aresta**. O peso de cada aresta corresponde à distância, em passos, entre aquelas duas portas. Esse peso é local e não representa a distância acumulada desde o `LABTEC`.

O projeto implementa quatro estratégias de busca e uma API em FastAPI para consultar as rotas encontradas.

## Integrantes

* Arthur Holz Leite
* Roger Pereira Soares
* Heitor Barbosa Hepp

## Estrutura do grafo

**Passos.** O ponto zero é o `LABTEC`.

O grafo tem **42 portas** e **59 arestas**.

As arestas são não direcionadas: uma ligação registrada entre `A` e `B` pode ser percorrida nos dois sentidos. Os dados ficam no arquivo `arestas.txt`, com uma aresta por linha:

```text
PORTA_A PORTA_B PESO
```

## Como rodar

```sh
python -m pip install -r requirements.txt
```

Conferir o grafo (número de portas e arestas, e se a BFS a partir do `LABTEC` alcança todas as portas):

```sh
python grafo.py
```

Comparar as buscas no terminal:

```sh
python buscas.py
```

Em seguida, informe a origem e o destino. Também é possível passar as portas diretamente:

```sh
python buscas.py LABTEC SAIDA_P2
```

Subir a API:

```sh
python -m uvicorn api:app --reload
```

Depois, abrir <http://127.0.0.1:8000/docs> para testar cada endpoint.

| Endpoint | Devolve |
|---|---|
| `GET /portas` | Todas as portas |
| `GET /vizinhos/{porta}` | Vizinhos e peso de cada aresta |
| `GET /rota?origem=&destino=&algoritmo=` | Caminho, custo e visitados (`bfs`, `dfs`, `gulosa` ou `dijkstra`) |
| `GET /comparar?origem=&destino=` | Os quatro algoritmos lado a lado |

Porta inexistente devolve **404** com mensagem. Algoritmo inexistente devolve **400**.

### Exemplos de requisições

Listar todas as portas:

```text
GET http://127.0.0.1:8000/portas
```

Encontrar a rota de menor custo com Dijkstra:

```text
GET http://127.0.0.1:8000/rota?origem=LABTEC&destino=SAIDA_P2&algoritmo=dijkstra
```

Comparar todas as buscas para o mesmo par de portas:

```text
GET http://127.0.0.1:8000/comparar?origem=LABTEC&destino=SAIDA_P2
```

Uma resposta de `/rota` tem este formato:

```json
{
	"algoritmo": "dijkstra",
	"caminho": [
		"LABTEC",
		"ACESSO_PATIO_1",
		"PREDIO_IDIOMAS",
		"SALA_207",
		"SALA_206",
		"SAIDA_P2"
	],
	"custo": 117,
	"unidade": "passos",
	"visitados": 42
}
```

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
| **Dijkstra** | Fila de prioridade (heap) | Escolhe a porta com menor custo acumulado conhecido e atualiza os custos dos vizinhos. |

### Dijkstra e o menor custo

O **Dijkstra** é o único algoritmo do projeto que garante o caminho de menor custo quando todos os pesos das arestas são não negativos, como ocorre neste grafo. Ele não procura necessariamente o caminho com menos portas: procura o caminho cuja soma dos pesos seja a menor possível.

O algoritmo começa com custo zero na origem e custo infinito nas demais portas. A cada passo, a fila de prioridade escolhe a porta com menor custo acumulado. Em seguida, o algoritmo verifica se passar por essa porta produz um caminho mais barato para cada vizinho. Quando uma porta é finalizada, seu menor custo já está confirmado.

Essa diferença é importante no mapa do prédio. A BFS pode escolher um caminho com poucas arestas, mesmo que uma delas seja longa. O Dijkstra pode passar por mais portas para evitar uma aresta muito pesada e, assim, chegar ao destino usando menos passos no total.

### O que cada busca devolve

Todas as buscas têm a mesma assinatura:

```python
funcao(grafo, origem, destino)
```

O retorno é uma tupla `(caminho, custo, visitados)`:

- **caminho:** portas percorridas da origem ao destino, na ordem em que aparecem na rota;
- **custo:** soma dos pesos das arestas do caminho, em passos;
- **visitados:** quantidade de portas examinadas até o destino ser encontrado.

Na BFS, uma porta é contada quando sai da fila. Na DFS e na busca gulosa, ela é contada quando é descoberta. No Dijkstra, ela é contada quando é finalizada, isto é, quando sai da fila de prioridade com seu menor custo confirmado.

Se não existir caminho entre as portas, o caminho retornado é vazio. Para uma porta de destino alcançável, o custo retornado pelo Dijkstra é o menor custo calculado para aquele destino.
