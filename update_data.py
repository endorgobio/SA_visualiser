import pandas as pd
import zeep
from zeep.helpers import serialize_object
import plotly.express as px

# read data from SIPSA
wsdl = 'http://appweb.dane.gov.co:9001/sipsaWS/SrvSipsaUpraBeanService?WSDL'
# convert data to dataframe
client = zeep.Client(wsdl=wsdl)

# # Get average price per city
# promAbas = client.service.promediosSipsaCiudad()
# promAbas = serialize_object(promAbas)
# df_precioProm = pd.DataFrame(promAbas)
# # change datatype for date columns
# df_precioProm['fechaCaptura'] = pd.to_datetime(df_precioProm['fechaCaptura'], utc=True).dt.date
# df_precioProm['fechaCreacion'] = pd.to_datetime(df_precioProm['fechaCreacion'], utc=True).dt.date
# # export the file to csv
# df_precioProm.to_csv("data/output.csv")

# #Get average harvest quantity per Department
# promRec = client.service.promediosSipsaParcial()
# promRec = serialize_object(promRec)
# df_promRec = pd.DataFrame(promRec)
# df_promRec['enmaFecha'] = pd.to_datetime(df_promRec['enmaFecha'], utc=True).dt.date
#
# #TODO: the merge below does not work without this writing/read
# df_promRec.to_csv("data/promRec.csv")
# df_promRec = pd.read_csv('data/promRec.csv')
# # Add city code and geocoding
# df_cities = pd.read_csv('data/DIVIPOLA_Municipios.csv',  sep=';')
# df_cities['muniId'] = df_cities['muniId'].astype(int)
# df_promRec = pd.merge(df_promRec, df_cities, on='muniId', how='left')
# df_promRec.to_csv("data/promRec.csv")




#dates = df_promRec['enmaFecha'].unique()
#print(dates)

# import pandas as pd
# import numpy as np
# import geopandas as gpd
# import matplotlib.pyplot as plt
#
# gdf = gpd.read_file('data\co_2018_MGN_MPIO_POLITICO.geojson')
# print(gdf.head())
#
# gdf_points = gdf.copy()
# gdf_points['geometry'] = gdf_points['geometry'].centroid
# gdf_points['MPIO_NAREA'] = gdf_points['MPIO_NAREA']/1000

# fig, ax = plt.subplots(figsize=(16,16))
# gdf.plot(ax=ax, color='lightgray', edgecolor='grey', linewidth=0.4)
# gdf_points.plot(ax=ax,color='#07424A', markersize='MPIO_NAREA',alpha=0.7, categorical=False, legend=True )
# ax.axis('off')
# plt.axis('equal')
# plt.show()


# gdf_points_4326 = gdf_points.to_crs('EPSG:4326')
# print(gdf_points_4326.geometry.y)
# fig = px.scatter_mapbox(
#                         gdf_points_4326,
#                         lat=gdf_points_4326.geometry.y,
#                         lon=gdf_points_4326.geometry.x,
#                         size='MPIO_NAREA',
#                         #color='MPIO_NAREA',
#                         #hover_name = 'MPIO_NAREA',
#                         #color_continuous_scale=px.colors.colorbrewer.Reds,
#                         #size_max=15,
#                         zoom=100
#                     )
# fig.show()
from plotly import graph_objs as go
import numpy as np
import configparser
#config = configparser.read('config.ini')
#mapbox_token = config['mapbox']['secret_token']


#df_filtered['LATITUD'].apply(lambda x: str(x.replace(',','.')))
#df_filtered['LATITUD'] = df_filtered['LATITUD'].astype(float, errors = 'raise')


# maxRec = df_filtered['promedioKg'].max()/50
# df_filtered['size'] = df_filtered['promedioKg']/maxRec
# # Create the figure and feed it all the prepared columns
# fig = go.Figure(
#     go.Scattermapbox(
#         lat=df_filtered['LATITUD'],
#         lon=df_filtered['LONGITUD'],
#         mode='markers',
#         marker=go.scattermapbox.Marker(
#             size=df_filtered['size'],
#             color=df_filtered['size'],
#             colorscale= 'Emrld'
#         )
#     )
# )
#
# # Specify layout information
# fig.update_layout(
#     mapbox=dict(
#         accesstoken='pk.eyJ1IjoiZW5kb3Jnb2JpbyIsImEiOiJja3M5bGs2MXUwNTlvMm9xOGQycjk1cTBiIn0.ziyGoWezFGUB_dnp4QHL6g', #
#         center=go.layout.mapbox.Center(lat=6.229523320626823, lon=-75.58190090468244),
#         zoom=5
#     )
# )






