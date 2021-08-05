import pandas as pd
import zeep
from zeep.helpers import serialize_object

# read data from SIPSA
wsdl = 'http://appweb.dane.gov.co:9001/sipsaWS/SrvSipsaUpraBeanService?WSDL'
client = zeep.Client(wsdl=wsdl)
promAbas = client.service.promediosSipsaCiudad()
promAbas = serialize_object(promAbas)
df_precioProm = pd.DataFrame(promAbas)
df_precioProm['fechaCaptura'] = pd.to_datetime(df_precioProm['fechaCaptura'], utc=True).dt.date
df_precioProm['fechaCreacion'] = pd.to_datetime(df_precioProm['fechaCreacion'], utc=True).dt.date
df_precioProm.to_csv("data/output.csv")