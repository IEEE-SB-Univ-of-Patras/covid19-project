# Imports
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

import datetime
import os
import sys
import Country_Dictionary


def return_dataframe(country):
    if country == "world":
        cases, deaths, active, dates = world_daily_data()
    else:
        debug_dictionary = {}
        Country_Dictionary.debug_country_dictionary_creator("country_names_urls.txt", debug_dictionary)
        url = Country_Dictionary.country_link_creator(debug_dictionary, country)
        cases, deaths, active, dates = country_daily_data(url)

    data = {'total cases': cases, 'total deaths': deaths, 'active cases': active}
    dataframe = pd.DataFrame(data, index=dates)

    return dataframe


def monthToNum(shortMonth):
    return {
        'Jan' : "01",
        'Feb' : "02",
        'Mar' : "03",
        'Apr' : "04",
        'May' : "05",
        'Jun' : "06",
        'Jul' : "07",
        'Aug' : "08",
        'Sep' : "09",
        'Oct' : "10",
        'Nov' : "11",
        'Dec' : "12"
        }[shortMonth]


def change_dates(dates):
    for i, date in enumerate(dates):
        date = date.split(" ")
        year = "2020"
        month = date[0]
        day = date[1]
        month = monthToNum(month)
        dates[i] = year + "-" + month + "-" + day


def country_daily_data(link):
    """ Scraps daily data about Covid-19 total cases, active cases and deaths, from worldometers.
        Arguments:
            -country (str)
        Outputs:
            -cases (list): total Covid-19 cases reported in the country day by day.
            -deaths (list): total Covid-19 deaths reported in the country day by day.
            -active (list): total Covid-19 active cases reported in the country day by day."""

    # Make sure that the country arg matches the url of the country you're looking for.
    # If not, make a special case

    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    # If this case is true, you need to make a special case for the country you're looking for.
    if "<title>404 Not Found</title>" in str(soup):
        print("Sorry, country not found!")
        sys.exit(1)

    # Locates the graphs we need from the page script
    js = soup.findAll("script", {"type": "text/javascript"})  # All the javascript bits
    for i, obj in enumerate(js):
        # Locates each graph by its title, which is contained somewhere in the script
        if "text: 'Total Cases'" in str(obj):
            cases_graph = str(obj).replace('\n', '')
        if "text: 'Total Deaths'" in str(obj):
            deaths_graph = str(obj).replace('\n', '')
        if "text: 'Active Cases'" in str(obj):
            active_graph = str(obj).replace('\n', '')

    # Finds the part that lists the daily numbers, and splits it into a list
    cases = re.findall('data: \[[0-9,]*\]', cases_graph)[0].split(": ")[1][1:-1].split(",")
    deaths = re.findall('data: \[[0-9,]*\]', deaths_graph)[0].split(": ")[1][1:-1].split(",")
    active = re.findall('data: \[[0-9,]*\]', active_graph)[0].split(": ")[1][1:-1].split(",")
    dates = re.findall('categories: \[[A-Za-z0-9," ]*\]', cases_graph)[0].split(": ")[1][1:-1].split(",")

    # Makes the elements of the list ints
    cases = [int(i) for i in cases]
    deaths = [int(i) for i in deaths]
    active = [int(i) for i in active]
    dates = [i.strip('"') for i in dates]
    change_dates(dates)

    return cases, deaths, active, dates


def world_daily_data():
    """ Scraps daily data about Covid-19 total cases, active cases and deaths, from worldometers.
        Arguments: None
        Outputs:
            -cases (list): total Covid-19 cases reported in the world day by day.
            -deaths (list): total Covid-19 deaths reported in the world day by day.
            -active (list): total Covid-19 active cases reported in the world day by day."""
    # For the total cases data
    LINK = "https://www.worldometers.info/coronavirus/"
    response = requests.get(LINK)
    soup = BeautifulSoup(response.text, "html.parser")

    # Locates the graphs we need from the page script
    js = soup.findAll("script", {"type": "text/javascript"})  # All the javascript parts of the page
    for i, obj in enumerate(js):
        # Finds the graph that lists total cases
        if "text: 'Total Cases'" in str(obj):
            cases_graph =str(obj).replace('\n', '')

    # Regular exp to extract the data and the values from Highcharts.chart
    values = re.findall('data: \[[0-9,]*\]', cases_graph)[0].split(": ")[1][1:-1].split(",")
    dates = re.findall('categories: \[[A-Za-z0-9," ]*\]', cases_graph)[0].split(": ")[1][1:-1].split(",")
    cases = [int(i) for i in values]
    dates = [i.strip('"') for i in dates]
    change_dates(dates)

    # For the deaths data
    LINK = "https://www.worldometers.info/coronavirus/coronavirus-death-toll/"
    response = requests.get(LINK)
    soup = BeautifulSoup(response.text, "html.parser")

    js = soup.findAll("script", {"type": "text/javascript"})
    for i, obj in enumerate(js):
        if "text: 'Total Deaths'" in str(obj):
            deaths_graph = str(obj).replace('\n', '')

    # regular exp to extract the data and the values from Highcharts.chart
    values_d = re.findall('data: \[[0-9,]*\]', deaths_graph)[0].split(": ")[1][1:-1].split(",")
    deaths = [int(i) for i in values_d]

    # For the active cases data
    LINK = "https://www.worldometers.info/coronavirus/coronavirus-cases/"
    response = requests.get(LINK)
    soup = BeautifulSoup(response.text, "html.parser")

    js = soup.findAll("script", {"type": "text/javascript"})
    for i, obj in enumerate(js):
        if "text: 'Active Cases'" in str(obj):
            active_graph = str(obj).replace('\n', '')

    # regular exp to extract the data and the values from Highcharts.chart
    values_a = re.findall('data: \[[0-9,]*\]', active_graph)[0].split(": ")[1][1:-1].split(",")
    active = [int(i) for i in values_a]

    return cases, deaths, active, dates


if __name__ == "__main__":
    df = return_dataframe("world")
    print(df)

