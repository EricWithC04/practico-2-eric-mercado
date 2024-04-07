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
    
    for pro in localidades_por_provincia:

        columnas = localidades_por_provincia[pro][0].keys()
        with open(f'localidades_provincias/{pro}.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columnas)
            writer.writeheader()
            
            writer.writerows(localidades_por_provincia[pro])