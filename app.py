import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from plotly import graph_objs as go
import numpy as np
import os



# read from github (already processed)
df_precioProm = pd.read_csv('https://raw.githubusercontent.com/endorgobio/SA_visualiser/master/data/output.csv', index_col=0)
df_promRec = pd.read_csv('https://raw.githubusercontent.com/endorgobio/SA_visualiser/main/data/promRec.csv')
df_promRec.reset_index(drop=True, inplace=True)

# Define the stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP,
    #'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap',
    #'https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet'
]

# Creates the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                title="Seguridad alimentaria",
                suppress_callback_exceptions=True)
# need to run it in heroku
server = app.server

# get data from the dataframe to be used in the layout
ciudades = df_precioProm['ciudad'].unique()
productos = df_precioProm['producto'].unique()
productos_dict =[{"label": k, "value": k} for k in productos]

# narratives narratives
filepath = os.path.split(os.path.realpath(__file__))[0]
# initial text
historia_text = open(os.path.join(filepath, "laHistoria.md"), "r").read()

reto_text = dcc.Markdown('''
* ** Reto 1**: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis et sapien eu purus malesuada rutrum non sed tortor. 
Phasellus iaculis
* **Reto 2**:  est massa feugiat ligula, sed facilisis urna arcu sit amet turpis. Maecenas malesuada 
neque eu felis eleifend accumsan. Nulla posuere cur
''')

# Final text
tab3_text = dcc.Markdown('''This is an interactive tool that allows to visualise the price of the agricultural products in the different  marketplaces in colombia. The information is taking from the [SIPSA](https://www.dane.gov.co/index.php/servicios-al-ciudadano/servicios-informacion/sipsa)  which is the plataform managed by Colombian Department for Statistics [DANE](https://www.dane.gov.co/) (Departamento Administrativo Nacional de Estadística DANE)

The file [Procfile](https://raw.githubusercontent.com/endorgobio/SA_visualiser/master/Procfile) specifies the commands that are executed by the app on startup. You can use a Procfile to declare a variety of process types, including Your app’s web server. [details](https://devcenter.heroku.com/articles/procfile)

The file [runtime](https://raw.githubusercontent.com/endorgobio/SA_visualiser/master/runtime.txt) specifies the python version to be run.

The file [requirements.txt](https://raw.githubusercontent.com/endorgobio/SA_visualiser/master/requirements.txt) provides the dependencies to be installed

The data is update daily using a [workflow](https://docs.github.com/es/actions/learn-github-actions) in github. The file in [update_data.yml](https://raw.githubusercontent.com/endorgobio/SA_visualiser/31c89961f1f4aff444fe2af3a51de96fd954951c/.github/workflows/update_data.yml) provides the details. It runs a python script with its own dependencies ([requerimentsGH.txt](https://raw.githubusercontent.com/endorgobio/SA_visualiser/master/requerimentsGH.txt)) that are installed when the action in the workflof is carried on

The user interface/dashboard is developed in Dash. A running version of it is avaibale at [https://savisualiser.herokuapp.com/](https://savisualiser.herokuapp.com/)
''')


controlsline_text = '''
    * Seleccione en el menú desplegable el producto de interes
    * En el gráfico active o desactive las ciudades que desea comparar
    '''
controls_line = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Markdown(children=controlsline_text),
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
    ]
)

controlsmap_text = '''
    * Seleccione en el menú desplegable el producto de interes
    * Seleccione la fecha que desea visualizar
    '''
controls_map = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Markdown(children=controlsmap_text),
                    dbc.FormGroup(
                        [
                            dcc.Dropdown(
                                id='prod-dropdown-map',
                                options=productos_dict,
                                value=productos[0]
                            ),
                        ]
                    ),
                    dbc.FormGroup(
                        [
                            dcc.DatePickerSingle(
                                id='date-picker',
                                min_date_allowed=df_promRec['enmaFecha'].min(),
                                max_date_allowed=df_promRec['enmaFecha'].max(),
                                initial_visible_month=df_promRec['enmaFecha'].min(),
                                date=df_promRec['enmaFecha'].max(),
                                display_format='DD/MM/YYYY',
                            ),
                        ]
                    )
                ]
            ),
        ),
    ]
)

tab1_content = dbc.Row([
        dbc.Col(dcc.Markdown(historia_text, dangerously_allow_html=True), md=8),
        dbc.Col(html.Div([
            #html.Img(src="/assets/images/banner_blue_text.png", className='banner_subsection'),
            html.Div(
                html.P("Los retos", className="header-description"),
                className="header_subsection1"),
            dbc.Card([
                dbc.CardBody([
                    html.P(
                        "Acceder diariamente de forma automática a la información publicada en"
                        "el SIPSA",
                        style={'textAlign': 'justify'},
                        className="card-text",
                    ),
                ])
            ]),
            dbc.Card([
                dbc.CardBody([
                    html.P(
                        "Generar una visualización interactiva que permita ver el histórico de precios de un"
                        "producto en las distintas centrales de abasto del país",
                        style={'textAlign': 'justify'},
                        className="card-text",
                    ),
                ])
            ]),
            dbc.Card([
                dbc.CardBody([
                    html.P(
                        "Diseñar una visualización que permita conocer las cantidades ofertadas de cada producto"
                        "en las distintas centrales de abasto del país",
                        style={'textAlign': 'justify'},
                        className="card-text",
                    ),
                ])
            ]),
        ]),
            md=4),
    ]
)

tab2_content = html.Div(
    [
        # Line graph and controls
        dbc.Row(
            className="row-with-margin",
            children=[
                dbc.Col(controls_line, md=3),
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

        dbc.Row(html.Div("                                 ")),
        # map graph and controls
        dbc.Row(
            [
                dbc.Col(controls_map, md=3),
                dbc.Col(
                    html.Div([
                        dcc.Graph(
                            id="chart_bubble",
                            #style={"height": 700}
                        )
                    ]),
                    md=9
                ),
            ],
            align="center",
        )
    ]
)

tab3_content = dbc.Row([
    dbc.Card(
        dbc.CardBody(
            [
                tab3_text
            ]
        )
    )
    ]
)


tabs_styles = {
    'height': '44px',
    'align-items': 'center'
}

tab_label_style = {
    'color' : 'black'
}

activetab_label_style = {
    'color': '#FD6E72',
    'fontWeight': 'bold'
}

ENDORGOBIO_LOGO = "assets/images/logo-Rojo.png"
INICIO = "assets/images/inicio.png"
POSTULATE = "assets/images/postulate.png"


back_bar = dbc.Row(
    [
        dbc.Col(
            html.A(
                dbc.Row(
                    [dbc.Col(html.Img(src=POSTULATE, height="30px")),],
                    align="center",
                    no_gutters=True,
                ),
            href="https://sites.google.com/view/proyectoendorgobio/post%C3%BAlate",
            ),
        ),
        dbc.Col(
            html.A(
                dbc.Row(
                    [dbc.Col(html.Img(src=INICIO, height="30px")),],
                    align="center",
                    no_gutters=True,
                ),
            href="https://sites.google.com/view/proyectoendorgobio/inicio",
            ),
        )
    ],
    no_gutters=False,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=ENDORGOBIO_LOGO, height="30px")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plotly.com",
        ),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            back_bar, id="navbar-collapse", navbar=True, is_open=False
        ),
    ],
    color="light",
    dark=True,
    fixed='top'
)


# Define the layout
app.layout = dbc.Container([
    navbar,
    dbc.Row(html.Img(src='assets/images/imagenBanner-Precios-de-alimentos1.jpg', style={'width': '100%'})),
    # Loading allows the spinner showing something is runing
    dcc.Loading(
        id="loading",
        # dcc.Store inside the app that stores the intermediate value
        children=[dcc.Store(id='data_solver'),
                  dcc.Store(id='data_solver_filtered')],
        fullscreen=True,
        type='circle'
    ),
    dbc.Tabs(
            [
                dbc.Tab(label="La historia", tab_id="historia", label_style=tab_label_style, active_label_style=activetab_label_style),
                dbc.Tab(label="La solución", tab_id="solucion", label_style=tab_label_style, active_label_style=activetab_label_style),
                dbc.Tab(label="Los detalles", tab_id="detalles", label_style=tab_label_style, active_label_style=activetab_label_style),
            ],
            id="tabs",
            active_tab="historia",
        ),
    dbc.Row(id="tab-content", className="p-4"),
    dbc.Row(html.Img(src='assets/images/pie-endorgobio.jpg', style={'width':'100%'})),
    ],
    fluid=True,
)

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab == "historia":
        return tab1_content
    elif active_tab == "solucion":
        return tab2_content
    elif active_tab == "detalles":
        return tab3_content

# Callback to update the graph
@app.callback(
    Output('chart', 'figure'),
    Input(component_id='prod-dropdown', component_property='value')
    )
def update_figure(selec_prod):
    # create empty dataframe to aggregate the dat for the different cities
    df = pd.DataFrame(columns=['fechaCaptura'])
    # filter dataframe for the chosen product
    df_filtered = df_precioProm[df_precioProm['producto'] == selec_prod]
    for ciudad in ciudades:
        # gets the data for the chosen product in ecah city
        dfT = df_filtered[(df_precioProm['ciudad'] == ciudad)][['fechaCaptura', 'precioPromedio']]
        # rename the column precioPromedio according to the particular city
        dfT = dfT.rename(columns={'precioPromedio': ciudad})
        # merge the dataframe for the different cities
        df = pd.merge(df, dfT, how="outer", on=["fechaCaptura", "fechaCaptura"])

    # Sort the values based on recording data
    df.sort_values(by=['fechaCaptura'], inplace=True)
    # create the figure
    fig = px.line(df, x='fechaCaptura', y=ciudades,
                  title="Precio por kg de {} en las distintas plazas de mercado".format(selec_prod),
                  labels={'value': 'precio (kg)',
                          'fechaCaptura': 'Fecha registro',
                          'variable': 'ciudad'}
                  )
    fig.update_layout(transition_duration=500)

    return fig



@app.callback(
    Output('chart_bubble', 'figure'),
    [Input(component_id='prod-dropdown-map', component_property='value'),
     Input(component_id='date-picker', component_property='date')]
    )

def update_figure_promRec(selec_prod, select_date):
    # filter dataframe for the chosen product and date
    df_filtered = df_promRec[(df_promRec['enmaFecha'] == select_date) & (df_promRec['artiNombre'] == selec_prod)][[
        'fuenNombre', 'promedioKg', 'LATITUD', 'LONGITUD']]
    maxRec = df_filtered['promedioKg'].max() / 50
    df_filtered['size'] = df_filtered['promedioKg'] / maxRec



    # Create the figure and feed it all the prepared columns
    fig = go.Figure(
        go.Scattermapbox(
            lat=df_filtered['LATITUD'],
            lon=df_filtered['LONGITUD'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=df_filtered['size'],
                color=df_filtered['size'],
                colorscale='Emrld',
                #showscale=True,
                #colorbar={'title': 'Kg recogidos', 'titleside': 'top', 'thickness': 4},
            ),
            customdata = np.stack(
                (pd.Series(df_filtered.index),
                 df_filtered['fuenNombre'],
                 df_filtered['promedioKg']),
                axis=-1
            ),
            hovertemplate = "<extra></extra>"
                            "<em>%{customdata[1]}</em><br>"
                            "Cantidad(kg): %{customdata[2]}",
        )
    )
    # Specify layout information
    fig.update_layout(
        title = "Cantidad (kg) recogida en las distintas plazas de mercado de {}".format(selec_prod),
        mapbox=dict(
            accesstoken='pk.eyJ1IjoiZW5kb3Jnb2JpbyIsImEiOiJja3M5bGs2MXUwNTlvMm9xOGQycjk1cTBiIn0.ziyGoWezFGUB_dnp4QHL6g',
            #
            center=go.layout.mapbox.Center(lat=6.229523320626823, lon=-75.58190090468244),
            zoom=4
        ),
        transition_duration=500
    )

    return fig


# main to run the app
if __name__ == "__main__":
    app.run_server(debug=True)
