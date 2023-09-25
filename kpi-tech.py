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
data_2019_to_2023 = df[(df['fecha_creacion'].dt.year >= 2019) & (df['fecha_creacion'].dt.year <= 2023)]

# Mostrar los resultados
print("-----------------------------------------------------------------------------------")
print("\n Data = 2019 to 2023")
print(data_2019_to_2023)


#filter (details & creation date)
print("-----------------------------------------------------------------------------------")
print("\n Details & creation date")
print(df.loc[:, ['detalle', "fecha_creacion"]])
print("-----------------------------------------------------------------------------------")
