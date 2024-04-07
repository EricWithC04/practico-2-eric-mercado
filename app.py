import csv
import sys
import MySQLdb

try:
    db = MySQLdb.Connect(host='localhost', user='root', password='', db='localidadesdb')
except MySQLdb.Error as err:
    print("No se pudo conectar a la base de datos:", err)
    sys.exit(1)
print("Conexión correcta.")

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

cursor = db.cursor()
create_table = "CREATE TABLE provincias (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255))"
nombres_provincias = list(localidades_por_provincia.keys())
create_table_localidades = "CREATE TABLE localidades (provincia INT, id INT PRIMARY KEY, localidad VARCHAR(255), cp VARCHAR(10), id_prov_mstr INT)"

try:
    # for prov in nombres_provincias:
    #     cursor.execute(f'INSERT INTO provincias (nombre) VALUES ("{prov}")')
    # cursor.execute(create_table)
    cursor.execute(create_table_localidades)
    db.commit()
except:
    db.rollback()

db.close()