import time
import json
import math
from random import random
from copy import deepcopy
from collections import Counter


from lector_csv import csv_to_dict, posiciones_to_dict, posicion_supermercado, \
     sensibilidad_to_float


class Feria:

    def __init__(self, calles=[]):
        self.inicio = None
        self.final = None

    def __repr__(self):
        return ", ".join(map(str, (e for e in self)))

    def __iter__(self):
        actual = self.inicio
        while actual is not None:
            yield actual
            actual = actual.siguiente

    def __getitem__(self, key):
        actual = self.inicio
        for i in range(key):
            actual = actual.siguiente
            if actual is None:
                raise KeyError
        return actual

    def __len__(self):
        c = 0
        for e in self:
            c += 1
        return c - 1

    def __eq__(self, other):
        if len(self) == len(other):
            for i in range(len(self)):
                if self[i] != other[i]:
                    return False
            return True
        return False                
        
    def agregar(self, esquina, checkear=False):
        if checkear:
            if esquina in self:
                raise Exception("No se puede agregar, ya esta en la feria")
        if self.inicio is None:
            self.inicio = esquina
            self.final = esquina
            return
        else:
            if self.final.es_adyacente(esquina):
                self.final.siguiente = esquina
                esquina.anterior = self.final
                self.final = esquina
            elif self.inicio.es_adyacente(esquina):
                self.inicio.anterior = esquina
                esquina.siguiente = self.inicio
                self.inicio = esquina
            else:
                raise Exception("No se puede agregar")

    def opciones(self):
        esquinas = self.inicio.adyacentes() + self.final.adyacentes()
        sin_repetir = []
        for esquina in esquinas:
            if esquina not in sin_repetir and esquina not in self:
                sin_repetir.append(esquina)
        return sin_repetir

    def copy(self):
        f = Feria()
        for e in self:
            f.agregar(Esquina(e.x, e.y))
        return f

    def mas_cercana(self, x, y):
        mejor_d = None
        mejor_e = None
        for e in self:
            d = e - Esquina(x, y)
            if mejor_d is None:
                mejor_d = d
                mejor_e = e
            if d < mejor_d:
                mejor_d = d
                mejor_e = e
        return mejor_e, mejor_d
        

class Esquina:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anterior = None
        self.siguiente = None

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def es_adyacente(self, other):
        return self - other == 1

    def adyacentes(self):
        x, y = self.x, self.y
        esquinas = [(x-1, y), (x+1, y), (x, y-1), (x,y+1)]
        esquinas = [Esquina(x, y) for x, y in esquinas if x >= 0 and y >= 0]
        return esquinas
        

        
def combinaciones(feria, limite=23, opciones=None):
    "Busca todas las combinaciones de 23 calles a partir de la esquina dada"
    if opciones is None:
        opciones = []
    if len(feria) >= limite:
        opciones.append(feria)
        return
    for esquina in feria.opciones():
        fc = feria.copy()
        fc.agregar(esquina)
        combinaciones(fc, limite, opciones)
    return opciones.copy()

def simular_ferias(ferias, limit=0):
    "Mejores n posiciones de la feria como un punto"
    ferias_counter = Counter()
    demanda = csv_to_dict("bdd/Semana 5.csv")
    posiciones = posiciones_to_dict()
    x_s, y_s = posicion_supermercado()
    s = sensibilidad_to_float()
    e = math.e
    c = 0
    for i, feria in enumerate(ferias):
        for calle, dias in demanda.items():
            x_c, y_c = posiciones[calle]
            df = feria.mas_cercana(x_c, y_c)[1]*100     # (esquina, distancia)
            ds = (abs(x_c - x_s) + abs(y_c - y_s))*100
            probabilidad = e**(df*s)/(e**(df*s)+e**(ds*s))
            for dia, tiendas in dias.items():
                if random() < probabilidad:
                    demanda_total = sum(v for v in tiendas.values())
                    ferias_counter[i] += demanda_total
        if limit != 0:
            c += 1
            if c == limit:
                break

    mejor = ferias[ferias_counter.most_common(1)[0][0]]

    return mejor

def buscar_mejor(calles_por_iteracion, tamaño_feria, mejores_n):
    print("Comenzamos")
    inicio = time.time()
    mejores_puntos = json.load(open('bdd/top10.json'))[:mejores_n]
    mejores_ferias = []
    with open("bdd/feria i{}t{}m{}.txt".format(
        calles_por_iteracion, tamaño_feria, mejores_n), "w") as fp:
        fp.write("Tamaño feria: {}\n".format(tamaño_feria))
        fp.write("Calles por iteracion: {}\n".format(calles_por_iteracion))
        fp.write("Cantidad de candidatos: {}\n".format(mejores_n))
    for dic in mejores_puntos:
        x, y = dic["posicion"]
        f = Feria()
        f.agregar(Esquina(math.floor(x), math.floor(y)))
        f.agregar(Esquina(math.ceil(x), math.ceil(y)))
        mejores_ferias.append(f)
    i = 1
    while i < tamaño_feria:
        i += calles_por_iteracion
        if i > tamaño_feria:
            i = tamaño_feria
        ferias = [f.copy() for f in mejores_ferias]
        mejores_ferias = []
        for feria in ferias:
            ferias = combinaciones(feria, i)
            feria = simular_ferias(ferias)
            if feria not in mejores_ferias:
                mejores_ferias.append(feria)
        inter = time.time()
        delta = time.strftime("Tiempo: %H:%M:%S", time.gmtime(inter-inicio))
        print("{} - Tamaño feria: {} - Cantidad ferias: {}".format(
            delta, i, len(mejores_ferias)))
        with open("bdd/feria i{}t{}m{}.txt".format(
            calles_por_iteracion, tamaño_feria, mejores_n), "a") as fp:
            fp.write(delta+"\n")
    mejor = simular_ferias(mejores_ferias)
    final = time.time()
    delta = time.strftime("Tiempo: %H:%M:%S", time.gmtime(final-inicio))
    
    print(mejor)
    with open("bdd/feria i{}t{}m{}.txt".format(
        calles_por_iteracion, tamaño_feria, mejores_n), "a") as fp:
        fp.write("\nFeria:\n")
        i = 0
        f = 0
        while f < tamaño_feria:
            f = i + 5
            if f > tamaño_feria:
                f = tamaño_feria
            for x in range(i, f):
                fp.write(str(mejor[x]))
            fp.write("\n")
            i += 5
        
    return mejor
            
        
    

if __name__ == "__main__":
    mejor = buscar_mejor(5, 23, 4)
