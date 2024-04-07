import csv

with open('localidades.csv') as archivo_csv:
    lector_csv = csv.reader(archivo_csv, delimiter=',', quotechar='"')
    cabecera = next(lector_csv)
    localidades = []

    for fila in lector_csv:
        loc = {}
        for i in range(len(cabecera)):
            loc[cabecera[i]] = fila[i]
        localidades.append(loc)

    localidades_por_provincia = {}

    for loc in localidades:
        if loc['provincia'] not in localidades_por_provincia:
            localidades_por_provincia[loc['provincia']] = []
        localidades_por_provincia[loc['provincia']].append(loc)
    
    for i in localidades_por_provincia:
        print(i, len(localidades_por_provincia[i]))