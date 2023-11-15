import pandas as pd
import numpy as np
import chardet
import json
import pytz
import requests
import plotly.express as px
from dash import Dash, Input, Output
from dash import dcc
from dash import html
import dash
import plotly.graph_objects as go


#LOAD DATASET
url = 'https://raw.githubusercontent.com/SEBASBELMOS/KPI-Tech/main/salida.json'
response = requests.get(url)
encoding = chardet.detect(response.content)['encoding']
data = response.content.decode(encoding)

tickets = [json.loads(line) for line in data.splitlines()]

df = pd.json_normalize(tickets)



#ETL
columnas_a_eliminar = ['_id', 'cliente._id', 'cliente.numero_identificacion', 'contacto.cargo', 'contacto.nombre', 'creador.cargo.__v', 'creador.cargo.consecutivo', 'creador.cargo.valor', 'creador.cargo.categoria', 'creador.cargo._id', 'creador.nombre', 'responsable._id', 'responsable.proceso._id', 'responsable.proceso.valor', 'responsable.tipo', 'responsable', 'responsable.proceso', 'creador.cargo', 'solucion.medio', 'solucion.medio._id', 'contacto', "responsable.numero_identificacion"]
df = df.drop(columnas_a_eliminar, axis=1)
df = df.dropna()

new_df = df[['fecha_server.$date', 'solucion.fecha_inicio', 'solucion.fecha_fin']].copy()
new_df['fecha_server.$date'] = pd.to_datetime(new_df['fecha_server.$date'])
colombia_tz = pytz.timezone('America/Bogota')
new_df['fecha_server.$date'] = new_df['fecha_server.$date'].dt.tz_convert(colombia_tz)
new_df['fecha_server.$date'] = pd.to_datetime(new_df['fecha_server.$date'], format='%Y-%m-%d %H:%M:%S')
colombia_tz = pytz.timezone('America/Bogota')
new_df['fecha_server.$date'] = new_df['fecha_server.$date'].dt.tz_convert(colombia_tz).dt.strftime('%Y-%m-%d %H:%M:%S')

d_df = new_df.copy()
d_df = d_df.astype(str)

d_df['fecha_server.$date'] = pd.to_datetime(d_df['fecha_server.$date'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
d_df['solucion.fecha_inicio'] = pd.to_datetime(d_df['solucion.fecha_inicio'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
d_df['solucion.fecha_fin'] = pd.to_datetime(d_df['solucion.fecha_fin'], format="%Y-%m-%d %H:%M:%S", errors='coerce')

d_df = d_df.dropna()



#PROMEDIOS
d_df["TPR"] = (d_df["solucion.fecha_fin"] - d_df["solucion.fecha_inicio"])
d_df["TPPR"] = (d_df["solucion.fecha_inicio"] - d_df['fecha_server.$date'])

tpr_promedio_minutos = np.mean(d_df["TPR"].dt.total_seconds() / 60)
tppr_promedio_minutos = np.mean(d_df["TPPR"].dt.total_seconds() / 60)

tpr_promedio_str = pd.to_timedelta(tpr_promedio_minutos, unit='m')
tppr_promedio_str = pd.to_timedelta(tppr_promedio_minutos, unit='m')

print("Tiempo Promedio de Resolución (TPR):", tpr_promedio_str)
print("Tiempo Promedio de Primera Respuesta (TPPR):", tppr_promedio_str)



#INFO FOR CHARTS
def extract_empresa(row):
    return row['cliente.nombre'] if row['cliente.nombre'] else None

cliente_counts = df.apply(extract_empresa, axis=1).value_counts()
tipo_soporte_counts = df['tipo_soporte'].value_counts()
estado_counts = df['estado'].value_counts()


#CHARTS

#BAR PLOT
fig_bar = go.Figure(data=go.Bar(x=d_df["solucion.fecha_inicio"], marker=dict(color='rgba(152, 0, 0, .8)')))
fig_bar.update_layout(title='Frecuencia de Tickets por Fecha de Inicio', xaxis_title='Fecha de Inicio', yaxis_title='Número de Tickets', barmode='overlay')

#SCATTER PLOT
fig_scatter = go.Figure(data=go.Scatter(x=d_df["solucion.fecha_inicio"], y=d_df["solucion.fecha_fin"], mode='markers', marker=dict(color='rgba(152, 0, 0, .8)')))
fig_scatter.update_layout(title='solucion.fecha_inicio vs solucion.fecha_fin', xaxis_title='solucion.fecha_inicio', yaxis_title='solucion.fecha_fin')

#BAR PLOT CLIENTE
fig_bar_cliente = go.Figure(data=go.Bar(x=cliente_counts.index, y=cliente_counts.values, marker_color='rgba(152, 0, 0, .8)'))
fig_bar_cliente.update_layout(title='Conteo de Tickets por Cliente', xaxis_title='Cliente', yaxis_title='Cantidad de Tickets')

#PIE PLOT ESTADO
fig_pie_estado = go.Figure(data=go.Pie(labels=estado_counts.index, values=estado_counts.values, marker_colors=['rgba(152, 0, 0, .8)', 'rgba(0, 152, 0, .8)', 'rgba(0, 0, 152, .8)']))
fig_pie_estado.update_layout(title='Distribución de Tickets por Estado')

#BAR PLOT TIPO SOPORTE
fig_bar_tipo_soporte = go.Figure(data=go.Bar(x=tipo_soporte_counts.index, y=tipo_soporte_counts.values, marker_color='rgba(152, 0, 0, .8)'))
fig_bar_tipo_soporte.update_layout(title='Conteo de Tickets por Tipo de Soporte', xaxis_title='Tipo de Soporte', yaxis_title='Cantidad de Tickets')



#DASH APP
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='graph-dropdown',
        options=[
            {'label': 'Scatter Plot', 'value': 'fig_scatter'},
            {'label': 'Bar Plot', 'value': 'fig_bar'},
            {'label': 'Bar Clientes Plot', 'value': 'fig_bar_cliente'},
            {'label': 'Pie Estado Plot', 'value': 'fig_pie_estado'},
            {'label': 'Bar Tipo Soporte Plot', 'value': 'fig_bar_tipo_soporte'},
        ],
        value='fig_scatter'
    ),
    dcc.Graph(id='graph')
])

@app.callback(
    Output('graph', 'figure'),
    [Input('graph-dropdown', 'value')]
)
def update_graph(graph_choice):
    if graph_choice == 'fig_scatter':
        return fig_scatter
    elif graph_choice == 'fig_bar':
        return fig_bar
    elif graph_choice == 'fig_bar_cliente':
        return fig_bar_cliente
    elif graph_choice == 'fig_pie_estado':
        return fig_pie_estado
    elif graph_choice == 'fig_bar_tipo_soporte':
        return fig_bar_tipo_soporte

if __name__ == '__main__':
    app.run_server(debug=True)