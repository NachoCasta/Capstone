import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import pandas as pd
import seaborn as sns

def generar_demanda_total(archivo="bdd/Histórico de Compras.csv",
                          output="bdd/Compras Totales.csv"):
    calles = {}
    with open(archivo, "r") as f:
        tiendas = f.readline().strip().split(";")[2:]
        ti = {tiendas[i]: i for i in range(len(tiendas))}
        for fila in f:
            fila = fila.strip().split(";")
            if fila[0] == "None":
                break
            calle = int(fila[1].split()[1])
            if not calle in calles:
                calles[calle] = {k: 0 for k in tiendas}
            for t in tiendas:
                calles[calle][t] += int(fila[2+ti[t]])
    with open(output, "w") as f:
        for i in range(len(calles)):
            f.write("Calle {}".format(i+1)+";")
            f.write(";".join(map(str, (calles[i+1][t] for t in tiendas)))+"\n")

def generar_graficos(archivo="bdd/Compras Totales.csv"):
    calles_pos = {}
    with open("bdd/Ciudad.csv", "r") as file:
        file.readline()
        for f in file:
            f = f.strip().split(";")
            calles_pos[f[0]] = ((int(f[1])+int(f[3]))/2,
                                (int(f[2])+int(f[4]))/2)
    calles_dem = {}
    with open(archivo, "r") as file:
        for f in file:
            f = f.strip().split(";")
            calles_dem[f[0]] = f[1:]
            
    tiendas = ['Verdulería', 'Carnicería', 'Frutería', 'Pescadería', 'Huevería',
               'Abarrotes', 'Florería', 'Ropa', 'Mascotería', 'Bazar']

    X, Y = np.array([]), np.array([])
    Z = []
    for i in range(len(tiendas)):
        Z.append(np.array([]))
    for i in range(len(calles_pos)):
        calle = "Calle {}".format(i+1)
        x, y = calles_pos[calle]
        
        X = np.append(X,x)
        Y = np.append(Y,y)
        for j in range(len(tiendas)):
            z = int(calles_dem[calle][j])
            Z[j] = np.append(Z[j],z)

    sns.set()

    fig,axn = plt.subplots(2, 5, sharex=True, sharey=True)

    for i in range(len(tiendas)):
        df = pd.DataFrame.from_dict(np.array([X,Y,Z[i]]).T)
        df.columns = ['X','Y','Z']
        df['Z'] = pd.to_numeric(df['Z'])
        pivotted= df.pivot('Y','X','Z')
        ax = axn.flat[i]
        ax.set_title(tiendas[i])
        sns.heatmap(pivotted,cmap='RdBu',ax=ax, vmin=20000, vmax=200000)
    plt.show()
        

if __name__ == "__main__":
    generar_demanda_total("bdd/Semana 5.csv", "bdd/Compras Totales Semana 5.csv")
    generar_graficos("bdd/Compras Totales Semana 5.csv")
