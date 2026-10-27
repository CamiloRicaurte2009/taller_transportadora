import math


class Paquete:
    def __init__(self, id, peso, alto, ancho, profundidad, destino, valor=1):
        self.id = id
        self.peso = peso                  
        self.alto = alto                  
        self.ancho = ancho                
        self.profundidad = profundidad    
        self.destino = destino            
        self.valor = valor                

    @property
    def volumen(self):
        return math.ceil(self.alto * self.ancho * self.profundidad / 1000)

    @property
    def peso_entero(self):
        return math.ceil(self.peso)

    def __repr__(self):
        return f"Paquete({self.id}, {self.peso}kg, {self.volumen}dm³, -> {self.destino})"


class Vehiculo:
    def __init__(self, tipo, peso_max, alto, ancho, profundidad):
        self.tipo = tipo                  
        self.peso_max = peso_max         
        self.alto = alto                  
        self.ancho = ancho                
        self.profundidad = profundidad    

    @property
    def volumen_max(self):
        return math.floor(self.alto * self.ancho * self.profundidad / 1000)

    def paquete_cabe(self, p):
        if p.peso > self.peso_max:
            return False
        dim_p = sorted([p.alto, p.ancho, p.profundidad])
        dim_v = sorted([self.alto, self.ancho, self.profundidad])
        return all(dp <= dv for dp, dv in zip(dim_p, dim_v))

    def __repr__(self):
        return f"Vehiculo({self.tipo}, {self.peso_max}kg, {self.volumen_max}dm³)"


def filtrar_paquetes(paquetes, vehiculo):
    aptos = [p for p in paquetes if vehiculo.paquete_cabe(p)]
    descartados = [p for p in paquetes if not vehiculo.paquete_cabe(p)]
    return aptos, descartados
