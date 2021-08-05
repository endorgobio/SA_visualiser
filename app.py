import pandas as pd
import plotly.express as px
import zeep
from zeep.helpers import serialize_object
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc

#
# wsdl = 'http://appweb.dane.gov.co:9001/sipsaWS/SrvSipsaUpraBeanService?WSDL'
# client = zeep.Client(wsdl=wsdl)
# promAbas = client.service.promediosSipsaCiudad()
#
# promAbas = serialize_object(promAbas)
# df_precioProm = pd.DataFrame(promAbas)
# df_precioProm['fechaCaptura'] = pd.to_datetime(df_precioProm['fechaCaptura'], utc=True).dt.date
# df_precioProm['fechaCreacion'] = pd.to_datetime(df_precioProm['fechaCreacion'], utc=True).dt.date
# df_precioProm.to_excel("output.xlsx")


df_precioProm = pd.read_excel('output.xlsx', index_col=0)

def update_figure(df_precioProm):
    ciudades = df_precioProm['ciudad'].unique()
    #ciudades = ['BARRANQUILLA', 'MEDELLÍN']
    df = pd.DataFrame(columns=['fechaCaptura'])

    for ciudad in ciudades:
        df_filtered = df_precioProm[(df_precioProm['ciudad'] == ciudad) & (df_precioProm['producto'] == 'Habichuela')][['fechaCaptura', 'precioPromedio']]
        #df_filtered.set_index('fechaCaptura', inplace=True)
        df_filtered = df_filtered.rename(columns={'precioPromedio': ciudad})
        #df = pd.concat([df, df_filtered], axis=1)
        df = pd.merge(df, df_filtered, how="outer", on=["fechaCaptura", "fechaCaptura"])

    df.sort_values(by=['fechaCaptura'], inplace=True)
    #fig = px.line(df, x='fechaCaptura', y='MEDELLÍN')
    #fig = px.line(df, x='fechaCaptura', y=['BARRANQUILLA', 'MEDELLÍN'])
    fig = px.line(df, x='fechaCaptura', y=ciudades,
                  title="Relación entre la tasa de recuperación y el requerimiento de materia prima",
                  labels={'value': 'precio(kg)'}
                  )
    fig.update_layout(transition_duration=500)

    return fig

fig_prices = update_figure(df_precioProm)
fig_prices.show()