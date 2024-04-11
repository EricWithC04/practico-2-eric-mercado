# Trabajo Practico N°2

## Instalación
Clonar el repositorio, luego en la misma carpeta crear un entorno virtual con el comando: 
```cmd
virtualenv {nombre_del_entorno}
``` 
Ingresar en la direccion del archivo `activate` con el comando:
```cmd
cd {nombre_del_entorno}/Scripts
```
Activar el entorno con el siguiente comando (CMD):
```cmd
.\activate
```
O también en bash:
```bash
source activate
```
Volver a la carpeta del proyecto con el comando:
```cmd
cd ../..
```
Instalar el driver de mysql con el comando: 
```cmd
pip install mysqlclient
```
Antes de ejecutar el codigo asegurate de crear una base de datos con el nombre `localidadesdb` en la base de datos mariadb, incluida en el paquete de xampp.  

Por último ejecutar el archivo:
```cmd
python app.py
```
Una vez realizados estos pasos se crearan los archivos csv en la carpeta `localidades_provincias`.