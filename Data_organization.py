import pandas as pd
import numpy as np
from worldometers import return_dataframe
from bs4 import BeautifulSoup
from io import StringIO
from datetime import date,timedelta
import requests

#Organizes data into dictionaries
def get_data_dicts():
    mobility_dataset,mobility_keys = mobility_data(0)
    
    measures_dataset, measures_keys =  measures_by_country(0)

    mobility_dict={}
    measures_dict={}
    worldometer_dict={}

    
    for i in mobility_keys:
        mobility_dict.update({i:mobility_dataset[i]})
    

    for i in measures_keys:
        measures_dict.update({i:measures_dataset[i]})

      
    return mobility_dict,measures_dict

#Returns the dataframe containing the information about the various political
#measures taken during the pandemic
def measures_by_country(country):
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

    


    return by_country,by_country.keys()


#Returns a dataframe containing the mobility data 
def mobility_data(country):

    days_ago=0
    while True:
        day=(date.today() - timedelta(days = days_ago)).strftime("%Y-%m-%d")
        source=requests.get("https://covid19-static.cdn-apple.com/covid19-mobility-data/2006HotfixDev16/v1/en-us/applemobilitytrends-" + day + ".csv")
        if source.ok:
            break
        days_ago+=1



    StringData = StringIO(source.text)



    mobility = pd.read_csv(StringData)



    mobility_countries = dict(tuple(mobility.groupby('geo_type')))['country/region']
    mobility_countries=mobility_countries.drop(columns=["transportation_type"]).groupby("region").mean()
    mobility_countries = mobility_countries.transpose()
    keys = mobility_countries.columns.values



    return mobility_countries,keys    


#Returns dataframe ready to enter the model    
def deliver_data():

    
    result_dict={}

    _,measures = get_data_dicts()

    static_dict=get_static()

    countries_mask=np.isin(static_dict.columns.values,list(measures.keys()))
##    countries=static_dict.columns.values[countries_mask]

    countries=['Italy','Germany','France','Spain','USA','Turkey','Russia','Iran','China','Brazil']
    
    for country in countries:
        try:
            worldometer_data=return_dataframe(country)
                    

            date_mask_min =measures[country].index>=min(worldometer_data.index)    
            country_measures=measures[country][date_mask_min]


            date_mask_max =country_measures.index<=max(worldometer_data.index)
            country_measures=country_measures[date_mask_max]
            

            ready = pd.concat([worldometer_data,country_measures],axis=1,join='inner')

            ready[ready.isnull()]=0



            for i in static_dict[country].index:
                ready[i]=[static_dict[country].loc[i]]*ready.shape[0]
            ################TEST##############
##            ready=ready.iloc[15:]
            ##################################
            result_dict.update({country:ready})
            print(country,'Done')
        except:
            print('ERROR LOADING',country)
        
    return result_dict

#Gets the static data for each country, returns a dictionary containing the dataframes
#for each country
def get_static():

    static_dict={}
    
    static = pd.read_csv('static.csv')
    static=static.transpose()
    static_index_mask = (static.index=='alpha3code')|(static.index=='firstcase')
    static=static[~static_index_mask]

    static=static.dropna(axis='columns')

    

    
    
    static.columns=static.loc['country']
    
    static=static.iloc[1:,1:]

    for i in [0,6,7]:
        for j in range(len(static.values[i])):
            static.values[i][j]=static.values[i][j].replace(',','')

    static=static.astype(float)

            
    for i in static.columns.values:
        static_dict.update({i:static[i]})



    return static

##deliver_data()
