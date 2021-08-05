import pandas as pd
import plotly.express as px
import zeep
from zeep.helpers import serialize_object
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


external_stylesheets = [dbc.themes.BOOTSTRAP,
    #'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                title="Seguridad alimentaria")
server = app.server

wsdl = 'http://appweb.dane.gov.co:9001/sipsaWS/SrvSipsaUpraBeanService?WSDL'
client = zeep.Client(wsdl=wsdl)
promAbas = client.service.promediosSipsaCiudad()

promAbas = serialize_object(promAbas)
df_precioProm = pd.DataFrame(promAbas)
df_precioProm['fechaCaptura'] = pd.to_datetime(df_precioProm['fechaCaptura'], utc=True).dt.date
df_precioProm['fechaCreacion'] = pd.to_datetime(df_precioProm['fechaCreacion'], utc=True).dt.date
df_precioProm.to_excel("output.xlsx")


#df_precioProm = pd.read_excel('output.xlsx', index_col=0)
ciudades = df_precioProm['ciudad'].unique()
productos = df_precioProm['producto'].unique()
productos_dict =[{"label": k, "value": k} for k in productos]

markdown_text = '''
Esta es una herramienta interactiva que visualizar los precios de los productos agrícolas en las distintas plazas de 
mercado del país. Para ello:
* Seleccione en el menú desplegable el producto de interes
* En el gráfico active o desactive las ciudades que desea comparar

Note que en aquellos casos en los que no se encuentra valor registrado en el SIPSA, el gráfico se presentará discontinuo
'''

controls = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.FormGroup(
                        [
                            dcc.Dropdown(
                                id='prod-dropdown',
                                options=productos_dict,
                                value=productos[0]
                            ),
                        ]
                    )
                ]
            ),
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Markdown(children=markdown_text)
                ]
            ),
        ),
    ]
)



app.layout = dbc.Container([
        html.Div(
            children=[
                html.H1(
                    children="Oferta-Demanda", className="header-title"
                ),
                html.P(
                    children="Herramientas de análisis del precio de los productos "
                             " agrícolas en las distintas plazas de mercado",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=3),
                dbc.Col(
                    html.Div([
                        dcc.Graph(
                                id="chart",
                                )
                    ]),
                    md=9
                ),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

@app.callback(
    Output('chart', 'figure'),
    Input(component_id='prod-dropdown', component_property='value')
    )
def update_figure(selec_prod):
    df = pd.DataFrame(columns=['fechaCaptura'])
    df_filtered = df_precioProm[df_precioProm['producto'] == selec_prod]
    for ciudad in ciudades:
        dfT = df_filtered[(df_precioProm['ciudad'] == ciudad)][['fechaCaptura', 'precioPromedio']]
        dfT = dfT.rename(columns={'precioPromedio': ciudad})
        df = pd.merge(df, dfT, how="outer", on=["fechaCaptura", "fechaCaptura"])

    df.sort_values(by=['fechaCaptura'], inplace=True)
    fig = px.line(df, x='fechaCaptura', y=ciudades,
                  title="Precio de {} en las distintas plazas de mercado".format(selec_prod),
                  labels={'value': 'precio (kg)',
                          'fechaCaptura': 'Fecha registro'}
                  )
    fig.update_layout(transition_duration=500)

    return fig



if __name__ == "__main__":
    app.run_server(debug=True)