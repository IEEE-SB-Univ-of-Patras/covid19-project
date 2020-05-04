import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO 



def measures_by_country():
        
    source=requests.get("https://oxcgrtportal.azurewebsites.net/api/CSVDownload")
    StringData = StringIO(source.text)

    
    
    measures = pd.read_csv(StringData)[['CountryName', 'CountryCode', 'Date', 'C1_School closing'
                                                               ,'C2_Workplace closing', 'C3_Cancel public events','C4_Restrictions on gatherings'
                                                               ,'C5_Close public transport','C6_Stay at home requirements','C7_Restrictions on internal movement',
                                                               'C8_International travel controls','StringencyIndex']]
    measures=measures.astype({'Date': str})
    for i in measures.index:
        val=str(measures.at[i,'Date'])
        measures.at[i,'Date']=val[:4]+'-'+val[4:6]+'-'+val[6:]

    by_country=dict(tuple(measures.groupby('CountryName')))
    for i in by_country:
        by_country[i].fillna(method='ffill', inplace=True)
        by_country[i]=by_country[i].drop(columns=['CountryName','CountryCode']).set_index('Date')

    


    return by_country




