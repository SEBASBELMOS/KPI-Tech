import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dash
import plotly.express as px
from dash import dcc, html, Input, Output
from dash.exceptions import PreventUpdate

# URL del archivo CSV
url = "https://drive.google.com/uc?export=download&id=1JjTg4mXMo5zMICLiPIfMajW3IWv51oUI" #fuente.csv

# Leer el DataFrame desde el archivo CSV
df = pd.read_csv(url, sep=',')

# Asesores a excluir
asesores_a_excluir = ['Comptel System Undefined', 'Tivisay Rubiano Quintero', 'Undefined Undefined', 'LEIDY CALAD BLANCO']

# Filtrar el DataFrame excluyendo a ciertos asesores
df = df[~df['responsable.nombre'].isin(asesores_a_excluir)]

# Convertir las columnas de fechas a tipo datetime
df['fecha_server.$date'] = pd.to_datetime(df['fecha_server.$date'], errors='coerce')

# Reemplazar nombres de asesores
df['responsable.nombre'] = df['responsable.nombre'].replace({'LEIDY CALAD BLANCO': 'Leidy Calad Blanco', 'SANTIAGO RUIZ VELASCO': 'Santiago Ruiz Velasco'})

df['solucion.fecha_inicio'] = pd.to_datetime(df['solucion.fecha_inicio'], errors='coerce')
df['solucion.fecha_fin'] = pd.to_datetime(df['solucion.fecha_fin'], errors='coerce')

# Eliminar filas con valores nulos en las columnas de fechas
df = df.dropna(subset=['solucion.fecha_inicio', 'solucion.fecha_fin'])

# Calcular la columna TPR_minutos
df['TPR_minutos'] = (df['solucion.fecha_fin'] - df['solucion.fecha_inicio']).dt.total_seconds() / 60

# Filtrar por TPR_minutos
df = df[df['TPR_minutos'] >= 0]
df = df[df['TPR_minutos'] <= 24 * 60]

# Calcular las columnas TPR y TPPR
df['TPR'] = df['solucion.fecha_fin'] - df['solucion.fecha_inicio']
df['TPPR'] = df['solucion.fecha_inicio'] - df['fecha_server.$date']

# Filtrar por horas en TPR y TPPR
df = df[(df['TPR'].dt.total_seconds() / 3600) <= 24]
df = df[(df['TPPR'].dt.total_seconds() / 3600) <= 24]

# Calcular tiempos promedio
tpr_promedio_minutos = np.mean(df['TPR'].dt.total_seconds() / 60)
tppr_promedio_minutos = np.mean(df['TPPR'].dt.total_seconds() / 60)

# YEAR MONTH
df['fecha_server.$date'] = pd.to_datetime(df['fecha_server.$date'])
df['YearMonth'] = df['fecha_server.$date'].dt.to_period('M')

# ASESOR NAME
df['responsable.nombre'] = df['responsable.nombre'].str.title()

df['responsable.nombre'].replace({
    'Santiago Ruiz Velasco': 'SANTIAGO RUIZ VELASCO',
    'Leydi Calad Blanco': 'LEIDY CALAD BLANCO'
}, inplace=True)

print(df['responsable.nombre'].unique())

# KPI FOR ASESOR
media_por_asesor = df.groupby('responsable.nombre')['TPR_minutos'].mean().round(0).astype(int)
frecuencia_valores = df['responsable.nombre'].value_counts()

# CANAL DE RESOLUCION
frec_canal = df['solucion.medio.valor'].value_counts()
print(frec_canal)

color_map = {
    'Jennifer Valencia Esquivel': '#1F77B4',
    'Luisa Maria Atehortua': '#FF7F0E',
    'Maria Victoria Murillo Prado': '#2CA02C',
    'Lina Marcela Vargas Quintero': '#D62728',
    'Juliana Katherine Pedraza Cardenas': '#9467BD',
    'Leidy Calad Blanco': '#8C564B',
    'Jean Carlos Quisoboni Jimenez': '#E377C2',
    'Andres Felipe Vera Cifuentes': '#7F7F7F',
    'Paul Andre Ruiz Caldas': '#BDBD34',
    'Jhonatan Galvis': '#17BECF',
    'Silvana Irene Bonilla Llano': '#BDBD34',
    'Santiago Ruiz Velasco': '#17BECF',
    'Bernardo Ruiz Caldas': '#D62728',
    'Miguel 0': '#FF9896',
    'Nathalia Rivera Posso': '#2CA02C'
}

asesores_media = media_por_asesor.index.tolist()
asesores_frecuencia = frecuencia_valores.index.tolist()

all_asesores = list(set(asesores_media + asesores_frecuencia))

# Charts
fig_media_por_asesor = px.bar(
    x=all_asesores,
    y=[media_por_asesor.get(a, 0) for a in all_asesores],
    color=all_asesores,
    labels={'x': 'Asesor', 'y': 'Media de tiempo en minutos'},
    title='Media de Tiempo Promedio de Resolución por Asesor',
    color_discrete_map=color_map
)

fig_frecuencia_valores = px.bar(
    x=all_asesores,
    y=[frecuencia_valores.get(a, 0) for a in all_asesores],
    color=all_asesores,
    labels={'x': 'Asesor', 'y': 'Frecuencia'},
    title='Frecuencia de Tickets por Asesor',
    color_discrete_map=color_map
)

fig_tpr = px.bar(
    x=['Tiempo Promedio de Resolución', 'Tiempo Promedio de Primera Respuesta'],
    y=[tpr_promedio_minutos, tppr_promedio_minutos],
    color=['indianred', 'lightsalmon'],
    labels={'x': 'Métrica', 'y': 'Tiempo (minutos)'},
    title='Tiempo Promedio de Resolución vs Tiempo Promedio de Primera Respuesta'
)

fig_solucion_medio_valor = px.bar(
    x=df['solucion.medio.valor'].value_counts().index,
    y=df['solucion.medio.valor'].value_counts().values,
    labels={'x': 'Medio de Valor', 'y': 'Cantidad'},
    title='Volumen de tickets por canal de soporte',
    color=df['solucion.medio.valor'].value_counts().index,
    color_discrete_map=color_map  
)

# Dash App
app = dash.Dash(__name__)

# Estilos CSS
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

app.layout = html.Div([
    html.H1("Análisis - PROYECTO KPI"),
    dcc.Tabs([
        dcc.Tab(label='Asesores', children=[
            html.Div([
                dcc.Graph(figure=fig_media_por_asesor),
                dcc.Graph(figure=fig_frecuencia_valores),
            ])
        ]),
        dcc.Tab(label='Tiempos', children=[
            html.Div([
                dcc.Graph(figure=fig_tpr),
                dcc.Graph(figure=fig_solucion_medio_valor),
            ])
        ]),
        dcc.Tab(label='Tickets Promedio', children=[
            html.Div([
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[
                        {'label': str(year), 'value': year} for year in df['fecha_server.$date'].dt.year.unique()
                    ],
                    value=df['fecha_server.$date'].dt.year.max()
                ),
                dcc.Graph(id='bar-chart')
            ])
        ])
    ])
])

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_graph(selected_year):
    filtered_df = df[df['fecha_server.$date'].dt.year == selected_year]
    avg_tickets_by_month = filtered_df.groupby('YearMonth').size().mean(level=0)

    fig = px.bar(
        x=avg_tickets_by_month.index.astype(str),
        y=avg_tickets_by_month.values,
        labels={'x': 'Mes-Año', 'y': 'Tickets Promedio'},
        title=f'Tickets Promedio por Mes en {selected_year}'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
