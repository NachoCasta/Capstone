from backtracking_feria import Feria, Esquina, simular_ferias

from copy import deepcopy


class Backtracking:

    def __init__(self, path):
        self.feria = self.open_feria(path)
        self.ferias = []
        self.largo_vereda = 13
        self.puestos = {
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
        self.cantidad = {
            1: 39,
            2: 18,
            3: 35,
            4: 16,
            5: 11,
            6: 15,
            7: 12,
            8: 13,
            9: 15,
            10: 13
            }
        self.originales = self.cantidad.copy()
        self.siguiente = locales(self.cantidad)
        self.mejor_u = 0

    def open_feria(self, path):
        feria = Feria(dist=True)
        i = 0
        with open(path, "r") as file:
            agregar = False
            for line in file:
                if "Feria:" in line:
                    agregar = True
                    continue
                if agregar:
                    i += 1
                    if line.strip() == "":
                        break
                    x, y = map(int, line.strip().split(" - ")[0][1:-1].split(", "))
                    e = Esquina(x, y)
                    e.orden = i
                    feria.agregar(e)
        return feria

    def prioridades(self):
        porcentaje = {
            k: self.cantidad[k]/self.originales[k]
            for k in self.cantidad
            }
        return sorted(list(self.cantidad.keys()),
                      key=lambda k: porcentaje[k],
                      reverse=True)

    def buscar(self, esquina):
        if esquina is None:
            raise Exception("Faltan calles")
        if not self.quedan_locales():
            f, u = simular_ferias(self.feria)
            f.utilidad = u
            self.ferias.append(deepcopy(f))
            if u > self.mejor_u:
                self.mejor_u = u
                print("{} - Mejor".format(u))
            else:
                print("{} - No es mejor".format(u))
            return True
        for vereda, otra in zip((esquina.vereda1, esquina.vereda2),
                                (esquina.vereda2, esquina.vereda1)):
            if 0 in vereda:
                i = vereda.index(0)
                break
        else:
            return self.buscar(esquina.siguiente)
        for local in self.prioridades():
            if self.cantidad[local] == 0:
                continue
            puestos = self.puestos[local]
            disponibles = self.largo_vereda - i
            if disponibles < puestos: # No cabe el local
                continue
            if i > 0:
                vecino = vereda[i-1]
                if not self.cumple_restricciones_vecinos(local, vecino):
                    continue
                diagonal = otra[i-1]
                if diagonal == local:
                    continue
            if i < self.largo_vereda - 1:
                diagonal = otra[i+1]
                if diagonal == local:
                    continue
            al_frente = False
            for x in range(i, i + puestos):
                if not self.cumple_restricciones_vecinos(local, otra[x]):
                    al_frente = True
            if al_frente:   # Restriccion con vecino de al frente
                continue
            for x in range(i, i + puestos):
                vereda[x] = local
            self.cantidad[local] -= 1
            if self.buscar(esquina):
                return True
            else:
                for x in range(i, i + puestos):
                    vereda[x] = 0
                self.cantidad[local] += 1
        return False

    def quedan_locales(self):
        return sum(self.cantidad.values()) > 0

    def cumple_restricciones_vecinos(self, p1, p2):
        if p1 == p2:            # Iguales
            return False
        if p1 == 3 and p2 == 4: # Fruteria, Pescaderia
            return False
        if p1 == 5 and p2 == 9: # Hueveria, Mascoteria
            return False
        if p1 == 6 and p2 == 10:# Abarrotes, Bazar
            return False
        return True

    def guardar_distribucion(self, feria, path):
        with open(path, "w") as file:
            string = ["", "", "", "", "", "", ""]
            for e in feria:
                for i in range(len(string)):
                    if i == 3:
                        string[i] += str(e)
                    else:
                        if e.orden == 1:
                            string[i] += " "*2
                        string[i] += " "*4
                if 0 not in e.vereda1 or 0 not in e.vereda2:
                    calle = e.to_map().split("\n")
                    for i in range(len(string)):
                        string[i] += calle[i]
                        if i == 3:
                            string[i] += (len(calle[2])-4)*" "
            for s in string:
                file.write(s + "\n")
        

def locales(cantidades):
    i = 0
    cero = False
    anterior = i
    while True:
        i += 1
        if i not in cantidades:
            i = 1
        if cantidades[i] > 0:
            yield i
        else:
            if sum(cantidades.values()) == 0:
                break
    yield None
                
if __name__ == "__main__":
    b = Backtracking("bdd/feria t23i1m4.txt")
    e = b.feria.inicio
##    e.vereda1 = [1,1,1,1,2,2,3,3,3,3,3,10,10]
##    e.vereda2 = [7,8,8,9,9,9,9,2,2,5,5,4,4]
    b.buscar(e)
    b.guardar_distribucion(b.feria, "bdd/distribucion factible.txt")
    
