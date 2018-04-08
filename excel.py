import pandas as pd

def excel_to_table(file, hoja):
    table = pd.read_excel(
        file, sheetname=hoja, header=1,
        parse_cols="B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q," + \
        " R, S, T, U, V, W, X, Y, Z")
##    fin = 0
##    for i in range(len(table)):
##        fila = table.iloc[i].real
##        nombre = fila[0]
##        fin = i
##        if str(nombre) == " " or str(nombre) == "nan" or str(nombre) == "":
##            break
##    tabla = table[0:fin]
    tabla = [[j for j in table.iloc[i].real]
             for i in range(len(table))]
    return tabla

def hojas(file="nuevo excel.xlsx"):
    excel = pd.ExcelFile(file)
    return excel.sheet_names

def excel_to_csv(file):
    for hoja in hojas(file):
        print("Comenzando {}".format(hoja))
        tabla = excel_to_table(file, hoja)
        with open("bdd/{}.csv".format(hoja), "w") as f:
            for fila in tabla:
                f.write(";".join(map(str, fila))+"\n")
        print("Creado {}.csv".format(hoja))


if __name__ == "__main__":
    excel_to_csv("bdd/Datos.xlsx")
