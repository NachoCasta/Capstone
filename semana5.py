import numpy as np

def lector_csv():
    calles = {}
    with open("bdd/Histórico de Compras.csv", "r") as file:
        tiendas = file.readline().strip().split(";")[2:]
        for line in file:
            line = line.strip().split(";")
            dia, calle, demandas = (int(line[0]), line[1],
                                   list(map(int, line[2:])))
            semana, dia = (dia-1)//7+1, (dia-1)%7+1
            if calle not in calles:
                calles[calle] = {}
            if semana not in calles[calle]:
                calles[calle][semana] = {}
            if dia not in calles[calle][semana]:
                calles[calle][semana][dia] = {}
            for tienda, demanda in zip(tiendas, demandas):
                d = calles[calle][semana][dia]
                d[tienda] = demanda
    return calles

def regresion_lineal(calle, producto):
    X = np.matrix([[1] + [calle[semana][dia][producto] for semana in range(1,4)]
                   for dia in range(1, 8)], dtype=np.int64)
    Y = np.matrix([[calle[4][dia][producto]] for dia in range(1,8)],
                  dtype=np.int64)
    Xt = np.transpose(X)
    XtX = np.matmul(Xt, X)
    XtXi = np.linalg.inv(np.matrix(XtX))
    B = (np.matmul(XtXi, np.matmul(Xt, Y)))
    X5 = np.matrix([[1] + [calle[semana][dia][producto] for semana in range(2,5)]
                   for dia in range(1, 8)], dtype=np.int64)
    Y5 = np.matmul(X5, B)
    return [round(i[0]) for i in Y5.tolist()]

def semana_5():
    calles = lector_csv()
    tiendas = ['Verdulería', 'Carnicería', 'Frutería', 'Pescadería', 'Huevería',
               'Abarrotes', 'Florería', 'Ropa', 'Mascotería', 'Bazar']
    for i in range(len(calles)):
        calle = calles["Calle {}".format(i+1)]
        calle[5] = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}}
        for producto in tiendas:
            s5 = regresion_lineal(calle, producto)
            for i in range(7):
                calle[5][i+1][producto] = s5[i]
    with open("bdd/Semana 5.csv", "w") as file:
        file.write("Día;Calle;" + ";".join(tiendas) + "\n")
        for dia in range(1, 8):
            for i in range(len(calles)):
                calle = "Calle {}".format(i+1)
                s = str(dia) + ";" + calle
                for tienda in tiendas:
                    s += ";" + str(calles[calle][5][dia][tienda])
                s += "\n"
                file.write(s)
        
    
if __name__ == "__main__":
    semana_5()
    
