import csv
from modelos import Paquete

COLUMNAS = {"id", "peso", "alto", "ancho", "profundidad", "latitud", "longitud"}


def cargar_paquetes(ruta_csv, grafo):
    paquetes = []
    ubicaciones = {} 

    with open(ruta_csv, newline="", encoding="utf-8-sig") as f:
        lector = csv.DictReader(f)
        faltantes = COLUMNAS - set(lector.fieldnames or [])
        if faltantes:
            raise ValueError(f"Faltan columnas en el CSV: {sorted(faltantes)}")

        for n, fila in enumerate(lector, start=2):
            try:
                lat, lon = float(fila["latitud"]), float(fila["longitud"])
                if not (4.3 <= lat <= 4.6 and -75.4 <= lon <= -75.1):
                    print(f"Aviso (línea {n}): ({lat}, {lon}) parece fuera de Ibagué")

                clave = (round(lat, 5), round(lon, 5))
                if clave not in ubicaciones:
                    nombre = (fila.get("nombre") or "").strip() or f"Dir_{len(ubicaciones) + 1}"
                    if nombre in grafo.coords:   
                        nombre = f"{nombre}_{len(ubicaciones) + 1}"
                    grafo.agregar_ubicacion(nombre, lat, lon)
                    ubicaciones[clave] = nombre

                paquetes.append(Paquete(
                    id=int(fila["id"]),
                    peso=float(fila["peso"]),
                    alto=float(fila["alto"]),
                    ancho=float(fila["ancho"]),
                    profundidad=float(fila["profundidad"]),
                    destino=ubicaciones[clave],
                    valor=int(fila.get("valor") or 1),
                ))
            except ValueError as e:
                print(f"Error en la línea {n}, se omite: {e}")

    return paquetes
