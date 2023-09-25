"Welcome to KPI TECH, this is our repository, follow our project"

import pandas as pd
import json

#Lectura del JSON
with open("C:/Users/sebas/OneDrive/Documentos/GitHub/KPI-Tech/salida.json", "r") as file:
    data = [json.loads(line) for line in file]

df = pd.DataFrame(data)
print(df)


# Convertir la columna 'fecha_creacion' al formato datetime
df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])

# Filtrar datos del año 2016 y 2022
datos_2016_2022 = df[(df['fecha_creacion'].dt.year == 2016) | (df['fecha_creacion'].dt.year == 2022)]

# Mostrar los resultados
print(datos_2016_2022)