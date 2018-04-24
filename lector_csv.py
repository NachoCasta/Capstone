def csv_to_dict(f):
    #calles -> dia -> tienda -> demanda
    calles = {}
    with open(f, "r") as file:
        tiendas = file.readline().strip().split(";")[2:]
        for line in file:
            line = line.strip().split(";")
            dia, calle, demandas = (int(line[0]), line[1],
                                   list(map(int, line[2:])))
            semana, dia = (dia-1)//7+1, (dia-1)%7+1
            if calle not in calles:
                calles[calle] = {}
            if dia not in calles[calle]:
                calles[calle][dia] = {}
            for tienda, demanda in zip(tiendas, demandas):
                d = calles[calle][dia]
                d[tienda] = int(demanda)
    return calles

def posiciones_to_dict():
    calles_pos = {}
    with open("bdd/Ciudad.csv", "r") as file:
        file.readline()
        for f in file:
            f = f.strip().split(";")
            calles_pos[f[0]] = ((int(f[1])+int(f[3]))/2,
                                (int(f[2])+int(f[4]))/2)
    return calles_pos
    
def posicion_supermercado():
    X, Y = 0, 0
    with open("bdd/Supermercado.csv", "r") as file:
        file.readline()
        for line in file:
            x, y = line.strip().split(";")
            X += int(x)
            Y += int(y)
    X /= 4
    Y /= 4
    return X, Y

def sensibilidad_to_float():
    with open("bdd/Sensibilidad.csv", "r") as file:
        file.readline()
        s = float(file.readline().strip())
    return s
    
