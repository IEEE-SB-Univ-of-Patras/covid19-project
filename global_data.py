''' data from https://www.kaggle.com/koryto/countryinfo#covid19tests.csv
    and https://www.apple.com/covid19/mobility '''
import pandas as pd

'''reading the csv and creating a dataframe with the necessary information'''

general=pd.read_csv(r"covid19_datasets\covid19countryinfo.csv")
general=general[["country","alpha3code","pop","density","medianage","urbanpop","smokers","lung","gdp2019","healthexp","healthperpop",
     "avgtemp","avghumidity","firstcase"]].drop(general.index[193:])


mobility=pd.read_csv(r"covid19_datasets\applemobilitytrends-2020-04-14.csv")
mobility_countries = dict(tuple(mobility.groupby('geo_type')))['country/region']#excluding cities
mobility_countries=mobility_countries.drop(columns=["transportation_type"]).groupby("region").mean()#merging the means of transportation rows and replacing it with their mean value

''' creating a csv for each dataframe and saving them in the cleaned_datasets folder'''
data={"general_country":general,"mobility_countries":mobility_countries}
for i in data:
    data[i].to_csv ('cleaned_datasets\\' + i + '.csv', index = True, header=True)

