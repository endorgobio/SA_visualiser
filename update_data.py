import pandas as pd
import zeep
from zeep.helpers import serialize_object


# read data from SIPSA
wsdl = 'http://appweb.dane.gov.co:9001/sipsaWS/SrvSipsaUpraBeanService?WSDL'
# convert data to dataframe
client = zeep.Client(wsdl=wsdl)

# # Get average price per city
promAbas = client.service.promediosSipsaCiudad()
promAbas = serialize_object(promAbas)
df_precioProm = pd.DataFrame(promAbas)
# change datatype for date columns
df_precioProm['fechaCaptura'] = pd.to_datetime(df_precioProm['fechaCaptura'], utc=True).dt.date
df_precioProm['fechaCreacion'] = pd.to_datetime(df_precioProm['fechaCreacion'], utc=True).dt.date
# export the file to csv
df_precioProm.to_csv("data/output.csv")

# Get average harvest quantity per Department
promRec = client.service.promediosSipsaParcial()
promRec = serialize_object(promRec)
df_promRec = pd.DataFrame(promRec)
df_promRec['enmaFecha'] = pd.to_datetime(df_promRec['enmaFecha'], utc=True).dt.date
df_promRec['muniId']=df_promRec['muniId'].astype(int)

# Add city code and geocoding
df_cities = pd.read_csv('https://raw.githubusercontent.com/endorgobio/SA_visualiser/master/data/DIVIPOLA_Municipios.csv',
                        sep=';',
                        encoding='unicode_escape')
df_cities['muniId'] = df_cities['muniId'].astype(int)
df_promRec = pd.merge(df_promRec, df_cities, on='muniId', how='left')
df_promRec.to_csv("data/promRec.csv")

