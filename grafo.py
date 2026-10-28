def carregar_grafo(caminho):
grafo = {}
with open(caminho, encoding="utf-8") as arq:
for linha in arq:
if not linha.strip():
continue
a, b, peso = linha.split()
peso = int(peso)
grafo.setdefault(a, []).append((b, peso))
grafo.setdefault(b, []).append((a, peso))
return grafo
