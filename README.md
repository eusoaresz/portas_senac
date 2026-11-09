# Rotas do Prédio com Grafos

Trabalho de **Algoritmos e Estruturas de Dados II**, desenvolvido a partir do mapeamento do prédio da UniSenac.

O prédio é representado por um grafo: cada **porta** é um nó e cada ligação entre duas portas vizinhas é uma **aresta**. O peso de cada aresta corresponde à distância, em passos, entre aquelas duas portas. Esse peso é local e não representa a distância acumulada desde o `LABTEC`.

O projeto implementa quatro estratégias de busca — BFS, DFS, busca gulosa e Dijkstra — e uma API em FastAPI para consultar as rotas encontradas.

## Integrantes

- Arthur Holz Leite
- Roger Pereira Soares
- Heitor Barbosa Hepp

## Estrutura do grafo

A unidade dos pesos é **passos**. O ponto zero da coleta é o `LABTEC`, mas qualquer porta cadastrada pode ser escolhida como origem de uma consulta.

O grafo tem **42 portas** e **59 arestas**. Todas as portas são alcançáveis a partir do `LABTEC`.

As arestas são não direcionadas: uma ligação registrada entre `A` e `B` pode ser percorrida nos dois sentidos. Os dados ficam no arquivo `arestas.txt`, com uma aresta por linha:

```text
PORTA_A PORTA_B PESO
```

Cada ligação é registrada uma única vez no arquivo. O carregador cria as duas entradas na lista de adjacência: de `A` para `B` e de `B` para `A`.

Por exemplo, `LABTEC SALA_201 3` e `SALA_201 SALA_202 3` representam dois trechos de 3 passos. O custo do caminho entre `LABTEC` e `SALA_202` por essas ligações é 6 passos.

## Arquivos do projeto

| Arquivo ou pasta | Função |
|---|---|
| `img/png/` | Imagens do mapeamento do prédio |
| `arestas.txt` | Ligações entre portas e seus pesos locais |
| `grafo.py` | Carregamento da lista de adjacência, contagem e conferência de conectividade |
| `buscas.py` | BFS, DFS, gulosa, Dijkstra e comparação pelo terminal |
| `api.py` | Endpoints da API FastAPI |
| `requirements.txt` | Dependências FastAPI e Uvicorn |

## Como rodar

Execute os comandos na pasta do repositório. Instale as dependências:

```sh
python -m pip install -r requirements.txt
```

Confira o número de portas e arestas e a conectividade a partir do `LABTEC`:

```sh
python grafo.py
```

Resultado esperado:

```text
Portas: 42
Arestas: 59
A BFS a partir do LABTEC alcança todas as portas.
```

Para comparar as buscas no terminal:

```sh
python buscas.py
```

Informe a origem e o destino quando solicitado. Digite `?` para consultar os nomes das portas. Também é possível passar as portas diretamente:

```sh
python buscas.py LABTEC ACESSO_PATIO_2
```

Para iniciar a API:

```sh
python -m uvicorn api:app --reload
```

Depois, abra [a documentação interativa da API](http://127.0.0.1:8000/docs) para testar cada endpoint.

## Endpoints

| Endpoint | Devolve |
|---|---|
| `GET /portas` | Todas as portas em ordem alfabética |
| `GET /vizinhos/{porta}` | Vizinhos e peso de cada aresta |
| `GET /rota?origem=&destino=&algoritmo=` | Caminho, custo e visitados de `bfs`, `dfs`, `gulosa` ou `dijkstra` |
| `GET /comparar?origem=&destino=` | Os quatro algoritmos para o mesmo par de portas |

Porta inexistente devolve **404** com mensagem. Algoritmo inexistente devolve **400**. A API aceita nomes de portas em minúsculas e remove espaços das extremidades, mas os nomes devem manter os sublinhados, como `SALA_201`.

### Exemplos de requisições

Listar todas as portas:

```text
GET http://127.0.0.1:8000/portas
```

Consultar os vizinhos do ponto zero:

```text
GET http://127.0.0.1:8000/vizinhos/LABTEC
```

Encontrar uma rota de menor custo com Dijkstra:

```text
GET http://127.0.0.1:8000/rota?origem=LABTEC&destino=ACESSO_PATIO_2&algoritmo=dijkstra
```

Para os dados atuais, o resultado dessa busca é:

```json
{
  "algoritmo": "dijkstra",
  "caminho": [
    "LABTEC",
    "SALA_201",
    "SALA_202",
    "SALA_203",
    "WC_FEMININO",
    "ACESSO_PATIO_2"
  ],
  "custo": 29,
  "unidade": "passos",
  "visitados": 9
}
```

Comparar todas as buscas para esse par de portas:

```text
GET http://127.0.0.1:8000/comparar?origem=LABTEC&destino=ACESSO_PATIO_2
```

## O que cada busca devolve

Todas as buscas têm a mesma assinatura:

```python
funcao(grafo, origem, destino)
```

O retorno é uma tupla `(caminho, custo, visitados)`:

- **caminho:** lista das portas da origem ao destino, na ordem da rota;
- **custo:** soma dos pesos das arestas da rota final, em passos;
- **visitados:** quantidade de portas examinadas segundo o critério de cada busca, incluindo o destino quando encontrado.

Uma rota com 6 portas tem 5 arestas. A quantidade de portas da rota e o número de visitados não representam o custo em passos.

| Busca | Estrutura | Critério de escolha | Contagem de visitados |
|---|---|---|---|
| **BFS** | Fila (`deque`) | Explora por camadas e encontra um caminho com o menor número de arestas; os pesos não orientam a escolha. | Conta cada porta quando sai da fila. |
| **DFS** | Pilha de chamadas recursivas | Aprofunda a busca no primeiro vizinho ainda não descoberto, seguindo a ordem da lista de adjacência. | Conta cada porta descoberta, pelas chaves de `anterior`. |
| **Gulosa** | Lista do caminho atual e lista de visitados | Escolhe o vizinho ainda não visitado com a menor aresta local; recua quando não há vizinhos novos. | Conta cada porta descoberta, mesmo que depois seja retirada do caminho atual. |
| **Dijkstra** | Fila de prioridade (`heapq`) | Escolhe a porta com menor custo acumulado conhecido e atualiza as distâncias dos vizinhos. | Conta cada porta finalizada; entradas repetidas descartadas da heap não contam novamente. |

O número de visitados pode ser maior que o número de portas da rota final, porque a busca pode examinar outros ramos. O custo retornado soma apenas a rota final, não os retrocessos feitos durante a exploração.

### Como funciona a busca gulosa deste projeto

A gulosa usa o peso da próxima aresta como critério local. Ela não utiliza uma estimativa de distância até o destino e não compara globalmente os custos acumulados de diferentes rotas.

Quando encontra um ponto sem vizinhos ainda não visitados, executa `caminho.pop()` e recua para a porta anterior. A porta retirada do caminho continua marcada em `visitados`, evitando novas explorações dela e ciclos.

Portanto, **há retrocesso em becos sem saída**, mas, ao encontrar o destino, a função retorna a rota encontrada e não continua procurando uma solução mais barata. A escolha local da menor aresta não garante o menor custo total. Nos empates de peso, prevalece o primeiro vizinho encontrado na lista.

### Dijkstra e o menor custo

O **Dijkstra** garante um caminho de menor custo para grafos com pesos não negativos, como o deste projeto. BFS, DFS e gulosa podem encontrar o mesmo custo em determinados casos, mas não oferecem essa garantia geral para pesos diferentes.

O algoritmo começa com custo zero na origem e custo infinito nas demais portas. A cada passo, a fila de prioridade fornece a porta com menor custo acumulado. Para cada vizinho, verifica se a distância atual somada ao peso da aresta é menor que a melhor distância conhecida. Se for, atualiza a distância e registra a porta anterior.

Quando uma porta é finalizada, seu menor custo está confirmado. A busca termina ao finalizar o destino e reconstrói o caminho pelos antecessores. Pode existir mais de uma rota com o mesmo custo mínimo; a função retorna uma delas.

## Exemplo em que BFS e Dijkstra encontram caminhos diferentes

No grafo do prédio, considere **origem `LABTEC` e destino `ACESSO_PATIO_2`**.

### Caminho encontrado pela BFS

```text
LABTEC → ACESSO_PATIO_1 → CANTINA_PORTA_1 → CANTINA_PORTA_2 → ACESSO_PATIO_2
```

- Pesos: `15 + 9 + 8 + 8 = 40 passos`.
- Quantidade de portas: **5**.
- Quantidade de arestas: **4**.
- Visitados: **16**.

### Caminho encontrado pelo Dijkstra

```text
LABTEC → SALA_201 → SALA_202 → SALA_203 → WC_FEMININO → ACESSO_PATIO_2
```

- Pesos: `3 + 3 + 10 + 9 + 4 = 29 passos`.
- Quantidade de portas: **6**.
- Quantidade de arestas: **5**.
- Visitados: **9**.

### Por que os resultados são diferentes?

A BFS minimiza o número de arestas. Por isso, encontra a rota de quatro ligações, mesmo que seus pesos somem 40 passos. O Dijkstra minimiza a soma dos pesos e encontra uma rota com uma ligação a mais, mas com custo de apenas 29 passos: **11 passos a menos**.

Isso não é um erro da BFS: os algoritmos usam critérios diferentes. Para os dados e a ordem atuais do arquivo, a comparação completa é:

| Algoritmo | Custo em passos | Portas na rota | Arestas na rota | Visitados |
|---|---:|---:|---:|---:|
| BFS | 40 | 5 | 4 | 16 |
| DFS | 29 | 6 | 5 | 6 |
| Gulosa | 29 | 6 | 5 | 6 |
| Dijkstra | 29 | 6 | 5 | 9 |

DFS e gulosa também encontram o custo mínimo nesse exemplo, mas isso não significa que o garantam para outros pares.

Para reproduzir:

```sh
python buscas.py LABTEC ACESSO_PATIO_2
```

Ou utilize `/comparar` na documentação interativa, com origem `LABTEC` e destino `ACESSO_PATIO_2`.

## Exemplo em que BFS e Dijkstra coincidem

Para `LABTEC → SAIDA_P2`, BFS e Dijkstra encontram a mesma rota:

```text
LABTEC → ACESSO_PATIO_1 → PREDIO_IDIOMAS → SALA_207 → SALA_206 → SAIDA_P2
```

O custo é `15 + 59 + 23 + 10 + 10 = 117 passos`.

| Algoritmo | Custo em passos | Portas na rota | Visitados |
|---|---:|---:|---:|
| BFS | 117 | 6 | 28 |
| DFS | 205 | 25 | 33 |
| Gulosa | 119 | 21 | 24 |
| Dijkstra | 117 | 6 | 42 |

Esse caso mostra que os critérios diferentes podem produzir a mesma rota. Também mostra que visitar menos portas não garante encontrar um caminho de menor custo.

## Observações sobre a implementação

- A ordem dos vizinhos vem da leitura de `arestas.txt`. Ela influencia as escolhas da DFS, os caminhos empatados da BFS e os empates locais da gulosa.
- Se origem e destino forem a mesma porta válida, as quatro buscas retornam uma lista contendo essa porta, custo zero e um visitado.
- O grafo atual é conectado. Se os dados forem alterados e não houver caminho entre duas portas válidas, BFS, DFS e gulosa retornam caminho vazio e custo zero; Dijkstra retorna caminho vazio e custo infinito. Nesse caso, zero não representa uma rota válida gratuita. O infinito precisaria ser tratado antes de produzir uma resposta JSON padrão pela API.
- O grafo é carregado quando o módulo da API é importado. Reinicie a aplicação após alterar `arestas.txt` para garantir que as consultas usem os novos dados.
- Os pesos representam passos medidos no mapeamento, e não tempo de percurso ou condições atualizadas de acesso.
