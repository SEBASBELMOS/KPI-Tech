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

# Filtrar datos del año 2019 al 2023
data_2019_to_2023 = df[(df['fecha_creacion'].dt.year >= 2019) & (df['fecha_creacion'].dt.year <= 2023)]

#filter (details & creation date)
print("\n data 2019 to 2023 with loc")
data_filtered = data_2019_to_2023.loc[:, ['detalle', "fecha_creacion"]]

# Mostrar los resultados
print("-----------------------------------------------------------------------------------")
print("\n Data = 2019 to 2023")
print(data_filtered.head(3))
print(data_filtered.tail(3))
print("-----------------------------------------------------------------------------------")

#sorted/date_data_descending 
sorted_data_desc = data_2019_to_2023.sort_values(by='fecha_creacion', ascending=False)
sorted_loc_data = sorted_data_desc.loc[:, ['detalle', "fecha_creacion"]]
print(" \nsorted/date_data_descending")
print(sorted_loc_data)
