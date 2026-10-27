import math
import heapq


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    f1, f2 = math.radians(lat1), math.radians(lat2)
    df = f2 - f1
    dl = math.radians(lon2 - lon1)
    a = math.sin(df / 2) ** 2 + math.cos(f1) * math.cos(f2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


class Grafo:
    FACTOR_VIAL = 1.3 

    def __init__(self):
        self.coords = {}   
        self.adj = {}      

    def agregar_nodo(self, nombre, lat, lon):
        self.coords[nombre] = (lat, lon)
        self.adj.setdefault(nombre, [])

    def conectar(self, a, b):
        
        d = round(haversine(*self.coords[a], *self.coords[b]) * self.FACTOR_VIAL, 2)
        self.adj[a].append((b, d))
        self.adj[b].append((a, d))

    def agregar_ubicacion(self, nombre, lat, lon, k=2):
        cercanos = sorted(
            self.coords,
            key=lambda n: haversine(lat, lon, *self.coords[n])
        )[:k]
        self.agregar_nodo(nombre, lat, lon)
        for c in cercanos:
            self.conectar(nombre, c)

    def dijkstra(self, origen):
        dist = {n: math.inf for n in self.adj}
        previo = {n: None for n in self.adj}
        dist[origen] = 0
        cola = [(0, origen)]

        while cola:
            d, u = heapq.heappop(cola)
            if d > dist[u]:
                continue
            for v, peso in self.adj[u]:
                nueva = d + peso
                if nueva < dist[v]:
                    dist[v] = nueva
                    previo[v] = u
                    heapq.heappush(cola, (nueva, v))
        return dist, previo

    def camino(self, origen, destino):
        dist, previo = self.dijkstra(origen)
        if dist[destino] == math.inf:
            return [], math.inf
        ruta, actual = [], destino
        while actual is not None:
            ruta.append(actual)
            actual = previo[actual]
        return ruta[::-1], round(dist[destino], 2)

    def matriz_distancias(self, nodos):
        matriz = {}
        for a in nodos:
            dist, _ = self.dijkstra(a)
            matriz[a] = {b: round(dist[b], 2) for b in nodos}
        return matriz


def crear_grafo_ibague():
    g = Grafo()

    lugares = {
        "Deposito": (4.4440, -75.2420),
        "Centro":   (4.4389, -75.2322),
        "Terminal": (4.4250, -75.2150),
        "U_Tolima": (4.4320, -75.2000),
        "La_Pola":  (4.4500, -75.2250),
        "Jordan":   (4.4600, -75.2150),
        "Picaleña": (4.4000, -75.1500),
        "Salado":   (4.4650, -75.2400),
        "Cádiz":    (4.4300, -75.2500),
    }
    for nombre, (lat, lon) in lugares.items():
        g.agregar_nodo(nombre, lat, lon)

    conexiones = [
        ("Deposito", "Centro"), ("Deposito", "Salado"), ("Deposito", "Cádiz"),
        ("Centro", "La_Pola"), ("Centro", "Terminal"), ("Centro", "Cádiz"),
        ("La_Pola", "Jordan"), ("La_Pola", "Salado"),
        ("Terminal", "U_Tolima"), ("U_Tolima", "Picaleña"),
        ("Jordan", "U_Tolima"),
    ]
    for a, b in conexiones:
        g.conectar(a, b)
    return g
