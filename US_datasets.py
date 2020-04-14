'''data from https://www.kaggle.com/jieyingwu/covid19-us-countylevel-summaries#healthcare_visits.csv'''

import pandas as pd
from datetime import date
import requests
from bs4 import BeautifulSoup

'''by city functions return a dict of dataframes'''

''' returns a dict containing each US state and its 2 letter abbreviation'''
def US_abbreviations():
    
    source=requests.get("https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations").text
    soup=BeautifulSoup(source,'lxml')
    table=soup.find_all('table')
    rows = soup.find_all('tr')[12:68]
    states_abbreviations={}
    
    for row in rows:
        cells = row.find_all('td')
        states_abbreviations.update({cells[3].text:cells[0].text.strip()})
        
    return states_abbreviations

'''returns a dataframe containing the cumulative sum of infections per day of each US city after some minor cleaning of the original csv'''
def US_infections_by_city():
    
    us_infections=pd.read_csv(r"covid19/infections_timeseries.csv").drop(columns=["FIPS"])
    us_infections['state'] = us_infections.apply(lambda row: str(row.Combined_Key).split('-')[1].strip(' '), axis = 1)#added a state column
    
    return dict(tuple(us_infections.groupby('state')))#contains each state and its corresponding cities

'''returns a dataframe containing the cumulative sum of infections per day of each US state after some minor cleaning of the original csv'''
def US_infections_by_state():
    
    us_infections=pd.read_csv(r"covid19/infections_timeseries.csv").drop(columns=["FIPS"])
    us_infections['state'] = us_infections.apply(lambda row: str(row.Combined_Key).split('-')[1].strip(' '), axis = 1)
    
    return us_infections.groupby('state').sum()

''' returns a dict containing each US city, its FIPS code and its state'''
def US_FIPS():
    
    us_infections=pd.read_csv(r"covid19/infections_timeseries.csv")
    us_infections['state'] = us_infections.apply(lambda row: str(row.Combined_Key).split('-')[1].strip(' '), axis = 1)
    
    return us_infections[["FIPS","Combined_Key","state"]].set_index("FIPS")

'''returns a dataframe containing the cumulative sum of deaths per day of each US city after some minor cleaning of the original csv
   simillar to the infections one'''
def US_deaths_by_city():
    
    us_deaths=pd.read_csv(r"covid19/deaths_timeseries.csv").drop(columns=["FIPS"])
    us_deaths['state'] = us_deaths.apply(lambda row: str(row.Combined_Key).split('-')[1].strip(' '), axis = 1)
    
    return dict(tuple(us_deaths.groupby('state')))


def US_deaths_by_state():
    
    us_deaths=pd.read_csv(r"covid19/deaths_timeseries.csv").drop(columns=["FIPS"])
    us_deaths['state'] = us_deaths.apply(lambda row: str(row.Combined_Key).split('-')[1].strip(' '), axis = 1)
    
    return us_deaths.groupby('state').sum()

'''contains the dates of interventions for each US city, measures taken to mitigate the spread'''
def US_interventions():
    states_abbreviations=US_abbreviations()
    
    us_interventions=pd.read_csv(r"covid19/interventions.csv").drop(columns=["FIPS"],index=[0])
    for i in list(us_interventions.columns)[2:]:
        us_interventions[i] = us_interventions[i].dropna().apply(int).apply(date.fromordinal)

    return us_interventions.apply(lambda row: states_abbreviations[row.STATE] , axis = 1)


def US_interventions_by_state():
    states_abbreviations=US_abbreviations()
    
    us_interventions=pd.read_csv(r"covid19/interventions.csv").drop(columns=["FIPS"],index=[0])
    for i in list(us_interventions.columns)[2:]:
        us_interventions[i] = us_interventions[i].dropna().apply(int).apply(date.fromordinal)
    us_interventions['STATE'] = us_interventions.apply(lambda row: states_abbreviations[row.STATE] , axis = 1)

    return us_interventions.groupby('STATE').first().drop(columns=["AREA_NAME"])
        
'''contains the number of people visiting  places of interest such as hospitals supermarkets etc, for each US city from 1/3 to 21/3'''
def US_poi_visits():
    FIPS=US_FIPS()
    us_poi_visits=pd.read_csv(r"covid19/poi_visits.csv").set_index("FIPS")
    '''added columns of US state and city it belongs'''
    us_poi_visits['state'] = None
    us_poi_visits['Combined_Key'] = None
    for i in us_poi_visits.index:
        try:us_poi_visits.at[i,'state']=FIPS.at[i,"state"]
        except:None
        try:us_poi_visits.at[i,'Combined_Key']=FIPS.at[i,'Combined_Key']
        except:None

    return us_poi_visits


def US_poi_visits_by_state():
    FIPS=US_FIPS()
    us_poi_visits=pd.read_csv(r"covid19/poi_visits.csv").set_index("FIPS")
    
    us_poi_visits['state'] = None
    us_poi_visits['Combined_Key'] = None
    for i in us_poi_visits.index:
        try:us_poi_visits.at[i,'state']=FIPS.at[i,"state"]
        except:None
        try:us_poi_visits.at[i,'Combined_Key']=FIPS.at[i,'Combined_Key']
        except:None

    return us_poi_visits.groupby('state').sum()


'''data from https://www.kaggle.com/sudalairajkumar/covid19-in-usa'''

def US_tests():
    tests=pd.read_csv(r"covid19\us_states_covid19_daily.csv")

    tests=tests.astype({'date': str}) #date format
    for i in range(2112):
        val=str(tests.at[i,'date'])
        tests.at[i,'date']=val[6:]+'/'+val[4:6]

    tests.drop(columns=["hospitalizedCurrently","recovered","hospitalizedCumulative","inIcuCurrently","inIcuCumulative", #unecessary information
                    "onVentilatorCurrently","onVentilatorCumulative","hash","dateChecked","death","hospitalized",
                    "deathIncrease","posNeg","hospitalizedIncrease","fips"],inplace=True)

    tests_per_state = dict(tuple(tests.groupby('state')))#groupby state, each state can be accessed as tests_per_state[state]
    for i in tests_per_state:
        tests_per_state[i].set_index("date",inplace=True)
        tests_per_state[i].drop(columns=["state"],inplace=True)

    return tests_per_state


