

import requests
import pandas as pd
from io import StringIO 



def mobility_data():

    version=requests.get("https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v2/index.json").json()
    url="https://covid19-static.cdn-apple.com"+version['basePath'] +version['regions']['en-us']['csvPath']

    source=requests.get(url)
    StringData = StringIO(source.text)



    mobility = pd.read_csv(StringData)



    mobility_countries = dict(tuple(mobility.groupby('geo_type')))['country/region']
    mobility_countries=mobility_countries.drop(columns=["transportation_type"]).groupby("region").mean()
    mobility_countries = mobility_countries.transpose()
    keys = mobility_countries.columns.values



    return mobility_countries




