import sys

from modelos import Vehiculo, filtrar_paquetes
from knapsack import knapsack_bottom_up
from grafo import crear_grafo_ibague
from ruta import orden_de_entrega
from cargador import cargar_paquetes

DEPOSITO = "Deposito"


def planificar_vehiculo(vehiculo, paquetes, grafo):
    aptos, _ = filtrar_paquetes(paquetes, vehiculo)      
    valor, elegidos = knapsack_bottom_up(aptos, vehiculo)           

    ruta, distancia = [], 0
    if elegidos:                                          
        destinos = [p.destino for p in elegidos]
        ruta, distancia, _, _ = orden_de_entrega(DEPOSITO, destinos, grafo)
    return valor, elegidos, ruta, distancia


def mostrar_plan(vehiculo, valor, elegidos, ruta, distancia, grafo):
    print("=" * 60)
    print(f"{vehiculo.tipo.upper()}  (máx {vehiculo.peso_max} kg, {vehiculo.volumen_max} dm³)")
    print("=" * 60)

    if not elegidos:
        print("No se pudo asignar ningún paquete.\n")
        return

    peso = sum(p.peso for p in elegidos)
    vol = sum(p.volumen for p in elegidos)
    print(f"Paquetes cargados: {len(elegidos)}  (valor total: {valor})")
    for p in elegidos:
        print(f"  #{p.id}: {p.peso} kg, {p.volumen} dm³ -> {p.destino}")
    print(f"Peso:    {peso:.1f} / {vehiculo.peso_max} kg")
    print(f"Volumen: {vol} / {vehiculo.volumen_max} dm³")

    print(f"\nOrden de entrega: {' -> '.join(ruta)}")
    print(f"Distancia total:  {distancia} km")

    print("\nEntregas por parada:")
    for parada in ruta[1:-1]:
        ids = [p.id for p in elegidos if p.destino == parada]
        print(f"  {parada}: paquetes {ids}")
    print()


def main():
    ruta_csv = sys.argv[1] if len(sys.argv) > 1 else "paquetes.csv"
    grafo = crear_grafo_ibague()

    moto = Vehiculo("moto", peso_max=30, alto=40, ancho=40, profundidad=50)
    carro = Vehiculo("carro", peso_max=500, alto=120, ancho=150, profundidad=200)

    pendientes = cargar_paquetes(ruta_csv, grafo)
    print(f"Paquetes cargados desde '{ruta_csv}': {len(pendientes)}\n")

    # La moto sale primero y toma lo que le sirve; el carro lleva el resto
    for vehiculo in (moto, carro):
        if not pendientes:
            break
        valor, elegidos, ruta, dist = planificar_vehiculo(vehiculo, pendientes, grafo)
        mostrar_plan(vehiculo, valor, elegidos, ruta, dist, grafo)
        ids = {p.id for p in elegidos}
        pendientes = [p for p in pendientes if p.id not in ids]

    if pendientes:
        print("Paquetes sin asignar:", pendientes)
    else:
        print("Todos los paquetes fueron asignados.")


if __name__ == "__main__":
    main()
