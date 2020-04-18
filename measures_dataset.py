'''data from https://github.com/OxCGRT/covid-policy-tracker'''

import pandas as pd



''' returns a dictionary, access each country's data as measures_countries()["Name of country"] '''
def measures_countries():
    # read the csv and drop any unwanted columns
    measures=pd.read_csv("covid19_datasets/OxCGRT_Download_140420_180452_Full.csv")[['CountryName', 'CountryCode', 'Date', 'S1_School closing'
                                                               ,'S2_Workplace closing', 'S3_Cancel public events','S4_Close public transport'
                                                               ,'S5_Public information campaigns','S6_Restrictions on internal movement',
                                                               'S7_International travel controls','StringencyIndex', 'StringencyIndexForDisplay']]

    # date formating
    measures=measures.astype({'Date': str})
    for i in measures.index:
        val=str(measures.at[i,'Date'])
        measures.at[i,'Date']=val[6:]+'/'+val[4:6]

    
    # turn the dataframe into a dict of dataframes, keys being the affected countries
    # and the value of each key being this country's measures
    by_country=dict(tuple(measures.groupby('CountryName')))
    for i in by_country:
        by_country[i].fillna(method='ffill', inplace=True) #fill NaN with the the last non-NaN of each column
        by_country[i]=by_country[i].drop(columns=['CountryName','CountryCode']).set_index('Date')

    return by_country


