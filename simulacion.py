import json
import math
from random import random
from collections import Counter
from pprint import PrettyPrinter

from lector_csv import csv_to_dict, posiciones_to_dict, posicion_supermercado, \
     sensibilidad_to_float

def feria_como_punto(n=10, limit=0):
    "Mejores n posiciones de la feria como un punto"
    calles = Counter()
    demanda = csv_to_dict("bdd/Semana 5.csv")
    posiciones = posiciones_to_dict()
    x_s, y_s = posicion_supermercado()
    s = sensibilidad_to_float()
    e = math.e
    c = 0
    print("Comienza simulación")
    for calle_f, pos_f in posiciones.items():
        x_f, y_f = pos_f
        for calle, dias in demanda.items():
            x_c, y_c = posiciones[calle]
            df = (abs(x_c - x_f) + abs(y_c - y_f))*100
            ds = (abs(x_c - x_s) + abs(y_c - y_s))*100
            probabilidad = e**(df*s)/(e**(df*s)+e**(ds*s))
            for dia, tiendas in dias.items():
                #if random() < probabilidad:
                demanda_total = sum(v for v in tiendas.values())
                calles[calle_f] += demanda_total*probabilidad
        if limit != 0:
            c += 1
            if c == limit:
                break
    print("Simulación lista")
    print("Buscando mejores {} resultados".format(n))
    mejores = calles.most_common(n)
    calles_mejores = [
        {"posicion": posiciones[c],
         "utilidad": u} for c, u in mejores
        ]
    
    with open("bdd/top10.json", "w") as fp:
        json.dump(calles_mejores, fp, indent=4)
        
    PrettyPrinter(indent=4).pprint(calles_mejores)

    return calles_mejores

if __name__ == "__main__":
    m = feria_como_punto()
