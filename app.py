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
    print("CSV leido correctamente.")

cursor = db.cursor()

create_table_localidades = "CREATE TABLE localidades (provincia VARCHAR(255), id INT, localidad VARCHAR(255), cp VARCHAR(10), id_prov_mstr INT)"

select_all_provinces = "SELECT provincia AS 'Provincia', COUNT(*) AS 'Localidades' FROM `localidades` GROUP BY provincia"

try:
    cursor.execute("DROP TABLE IF EXISTS localidades")
    cursor.execute(create_table_localidades)
    print("Tabla creada con exito.")

    for loc in localidades:
        cursor.execute(f'INSERT INTO localidades (provincia, id, localidad, cp, id_prov_mstr) VALUES ("{loc["provincia"]}", {loc["id"]}, "{loc["localidad"]}", "{loc["cp"]}", {loc["id_prov_mstr"]})')
    db.commit()
    print("Registros insertados con exito.")

    cursor.execute(select_all_provinces)
    provinces_localities = dict(cursor.fetchall())

    all_provinces = list(provinces_localities.keys())

    for prov in all_provinces:
        cursor.execute(f'SELECT * FROM localidades WHERE provincia = "{prov}"')
        locs = list(cursor.fetchall())
        with open(f'localidades_provincias/{prov}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(cabecera)
            writer.writerows(locs)
            writer.writerow(["Total de localidades: " + str(provinces_localities[prov])])
    print("CSVs creados con exito.")
    
except Exception as e:
    print("Error: ", e)
    db.rollback()

db.close()