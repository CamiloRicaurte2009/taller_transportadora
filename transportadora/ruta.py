
class UnionFind:
    def __init__(self, elementos):
        self.padre = {e: e for e in elementos}
        self.rango = {e: 0 for e in elementos}

    def find(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.find(self.padre[x]) 
        return self.padre[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False  
        if self.rango[ra] < self.rango[rb]:
            ra, rb = rb, ra
        self.padre[rb] = ra
        if self.rango[ra] == self.rango[rb]:
            self.rango[ra] += 1
        return True


def kruskal(nodos, matriz):
    aristas = []
    for i, a in enumerate(nodos):
        for b in nodos[i + 1:]:
            aristas.append((matriz[a][b], a, b))
    aristas.sort()

    uf = UnionFind(nodos)
    mst, costo = [], 0
    for d, a, b in aristas:
        if uf.union(a, b):
            mst.append((a, b, d))
            costo += d
            if len(mst) == len(nodos) - 1:
                break
    return mst, round(costo, 2)


def dfs_preorden(arbol, nodo, visitados, orden, matriz):
    visitados.add(nodo)
    orden.append(nodo)
    for vecino in sorted(arbol[nodo], key=lambda v: matriz[nodo][v]):
        if vecino not in visitados:
            dfs_preorden(arbol, vecino, visitados, orden, matriz)


def orden_de_entrega(deposito, destinos, grafo):

    nodos = [deposito] + [d for d in dict.fromkeys(destinos) if d != deposito]
    matriz = grafo.matriz_distancias(nodos)

    mst, costo_mst = kruskal(nodos, matriz)

    arbol = {n: [] for n in nodos}
    for a, b, _ in mst:
        arbol[a].append(b)
        arbol[b].append(a)

    orden = []
    dfs_preorden(arbol, deposito, set(), orden, matriz)

    ruta = orden + [deposito]
    total = round(sum(matriz[ruta[i]][ruta[i + 1]] for i in range(len(ruta) - 1)), 2)
    return ruta, total, mst, costo_mst
