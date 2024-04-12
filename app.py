import csv
import sys
import MySQLdb

# Conectamos con la base de datos
try:
    db = MySQLdb.Connect(host='localhost', user='root', password='', db='localidadesdb')
except MySQLdb.Error as err:
    print("No se pudo conectar a la base de datos:", err)
    sys.exit(1)
print("Conexión correcta.")

# Leemos el archivo CSV y le damos formato de diccionario
with open('localidades.csv') as archivo_csv:
    lector_csv = csv.reader(archivo_csv, delimiter=',', quotechar='"')
    cabecera = next(lector_csv)
    localidades = []

    for fila in lector_csv:
        localidades.append(fila)
    print("CSV leido correctamente.")

cursor = db.cursor()

# Todas las consultas para la base de datos
create_table_localidades = "CREATE TABLE localidades (provincia VARCHAR(255), id INT, localidad VARCHAR(255), cp VARCHAR(10), id_prov_mstr INT)"

select_all_provinces = "SELECT provincia AS 'Provincia', COUNT(*) AS 'Localidades' FROM `localidades` GROUP BY provincia"

drop_if_exists = "DROP TABLE IF EXISTS localidades"

insert_localidades = 'INSERT INTO localidades (provincia, id, localidad, cp, id_prov_mstr) VALUES (%s, %s, %s, %s, %s)'

select_localidades = 'SELECT * FROM localidades WHERE provincia = %s'

try:
    # Si la tabla ya existe, la borramos y la volvemos a crear
    cursor.execute(drop_if_exists)
    cursor.execute(create_table_localidades)
    print("Tabla creada con exito.")

    # Insertamos todos los registros de localidades
    cursor.executemany(insert_localidades, localidades)
    db.commit()
    print("Registros insertados con exito.")

    # Traemos todas las provincias junto con la cantidad de localidades de cada una
    cursor.execute(select_all_provinces)
    provinces_localities = dict(cursor.fetchall())

    all_provinces = list(provinces_localities.keys())

    # Traemos todas las localidades de cada una de las provincias
    for prov in all_provinces:
        cursor.execute(select_localidades, [prov])
        locs = list(cursor.fetchall())

        # Escribimos los resultados en un archivo CSV para cada una de las provincias, 
        # primero la cabecera, todas las localidades y por ultimo el total de localidades
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