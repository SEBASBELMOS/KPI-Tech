import json

#read json
with open('salida.json', 'r') as archivo_json:
    datos_json = json.loads(archivo_json)

#load data
#se puede utilizar bibliotecas como sqlite3, SQLAlchemy, pymysql
#with open('nuevo_archivo.json', 'w') as archivo_salida:
    #json.dump(datos_transformados, archivo_salida, indent=4)

print(archivo_json)
