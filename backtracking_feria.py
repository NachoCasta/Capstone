import time
import json
import math
from random import random
from copy import deepcopy
from collections import Counter


from lector_csv import csv_to_dict, posiciones_to_dict, posicion_supermercado, \
     sensibilidad_to_float


class Feria:

    def __init__(self, dist=False):
        self.inicio = None
        self.final = None
        self.largo = 0
        self.dist = dist

    def __repr__(self):
        return ", ".join(map(str, (e for e in self)))

    def to_map(self):
        s = ""
        for e in self:
            s += e.to_map()
            s += "\n" + "-"*27 + "\n\n"
        return s

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
        return self.largo

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
        else:
            self.largo += 1
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
        if esquina.orden is None:
            esquina.orden = self.largo

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
            
            f.agregar(e.copy())
        return f

    def mas_cercana(self, x, y):
        if not self.dist:
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
        else:
            mejores = []
            for i in range(1, 11):
                mejor_d = None
                mejor_e = None
                for e in self:
                    if i in e.vereda1 or i in e.vereda2:
                        d = e - Esquina(x, y)
                        if mejor_d is None:
                            mejor_d = d
                            mejor_e = e
                        if d < mejor_d:
                            mejor_d = d
                            mejor_e = e
                mejores.append((mejor_e, mejor_d))
            mejores.sort(key=lambda k: k[1], reverse=True)
            return mejores[0]
        

class Esquina:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anterior = None
        self.siguiente = None
        self.orden = None
        self.vereda1 = [0 for i in range(13)]
        self.vereda2 = [0 for i in range(13)]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def to_map(self):
        nombres = {
            0: " ",
            1: "Verduleria",
            2: "Carniceria",
            3: "Fruteria",
            4: "Pescaderia",
            5: "Hueveria",
            6: "Abarrotes",
            7: "Floreria",
            8: "Ropa",
            9: "Mascoteria",
            10: "Bazar"
            }
        puestos = {
            0: 1,
            1: 4,
            2: 2,
            3: 5,
            4: 2,
            5: 2,
            6: 3,
            7: 1,
            8: 2,
            9: 4,
            10: 2
            }
        s = ""
        vl = ""
        v = ""
        ultimo = ""
        for p in self.vereda1:
            if ultimo == p and p != 0:
                continue
            c = puestos[p]
            vl += "+" + (2*c-1)*"-"
            v += "|"
            v += ("{0: ^"+str(2*c-1)+"}").format(cortar(nombres[p], 2*c-1))
            ultimo = p
        s += vl + "+\n"
        s += v + "|\n"
        s += vl + "+\n"
        s += "\n"
        vl = ""
        v = ""
        ultimo = ""
        for p in self.vereda2:
            if ultimo == p and p != 0:
                continue
            c = puestos[p]
            vl += "+" + (2*c-1)*"-"
            v += "|"
            v += ("{0: ^"+str(2*c-1)+"}").format(cortar(nombres[p], 2*c-1))
            ultimo = p
        s += vl + "+\n"
        s += v + "|\n"
        s += vl + "+\n"
        return s

    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def es_adyacente(self, other):
        return self - other == 1

    def adyacentes(self):
        x, y = self.x, self.y
        esquinas = [(x-1, y), (x+1, y), (x, y-1), (x,y+1)]
        esquinas = [Esquina(x, y) for x, y in esquinas if x >= 0 and y >= 0]
        return esquinas

    def copy(self):
        e = Esquina(self.x, self.y)
        e.orden = self.orden
        return e
        
def cortar(string, largo_max):
    if len(string) > largo_max:
        return string[:largo_max]
    else:
        return string
    
        
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
    if type(ferias) != list:
        ferias = [ferias]
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
##                if random() < probabilidad:
##                    demanda_total = sum(v for v in tiendas.values())
##                    ferias_counter[i] += demanda_total
                demanda_total = sum(v for v in tiendas.values())
                ferias_counter[i] += demanda_total*probabilidad
        if limit != 0:
            c += 1
            if c == limit:
                break

    contador = ferias_counter.most_common(1)[0]
    mejor = ferias[contador[0]], contador[1]

    #print(ferias_counter.most_common(1)[0][1])

    return mejor

def buscar_mejor(calles_por_iteracion, tamaño_feria, mejores_n):
    print("Comenzamos")
    inicio = time.time()
    mejores_puntos = json.load(open('bdd/top10.json'))[:mejores_n]
    mejores_ferias = []
    with open("bdd/feria t{1}i{0}m{2}.txt".format(
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
            feria, _ = simular_ferias(ferias)
            if feria not in mejores_ferias:
                mejores_ferias.append(feria)
        inter = time.time()
        delta = time.strftime("Tiempo: %H:%M:%S", time.gmtime(inter-inicio))
        print("{} - Tamaño feria: {} - Cantidad ferias: {}".format(
            delta, i, len(mejores_ferias)))
        with open("bdd/feria t{1}i{0}m{2}.txt".format(
            calles_por_iteracion, tamaño_feria, mejores_n), "a") as fp:
            fp.write(delta+"\n")
    mejor, utilidad = simular_ferias(mejores_ferias)
    final = time.time()
    delta = time.strftime("Tiempo: %H:%M:%S", time.gmtime(final-inicio))
    
    with open("bdd/feria t{1}i{0}m{2}.txt".format(
        calles_por_iteracion, tamaño_feria, mejores_n), "a") as fp:
        fp.write("\nFeria:\n")
        for e in mejor:
            fp.write("{} - {}\n".format(e, e.orden))
            print("{} - {}".format(e, e.orden))
        fp.write("\nUtilidad: ${:,}".format(round(utilidad)).replace(",", "."))
        
    return mejor
            
        
    

if __name__ == "__main__":
    #mejor = buscar_mejor(5, 23, 4)
    pass
