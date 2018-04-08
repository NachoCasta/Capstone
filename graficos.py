def generar_demanda_total():
    calles = {}
    with open("bdd/Histórico de Compras.csv", "r") as f:
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
    with open("bdd/Compras Totales.csv", "w") as f:
        for i in range(len(calles)):
            f.write("Calle {}".format(i+1)+";")
            f.write(";".join(map(str, (calles[i+1][t] for t in tiendas)))+"\n")
              
            

if __name__ == "__main__":
    generar_demanda_total()
