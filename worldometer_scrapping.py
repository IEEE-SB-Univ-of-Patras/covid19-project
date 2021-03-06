# -*- coding: utf-8 -*-
"""Worldometers Scrapping

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h4ieSGCHonYbmReYxbV9AhjJz-SA1Fou
"""

# Imports
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

import datetime
import os
import sys


def up_to_date(scope="world"):
    """ Checks whether the requested data is up to date.
        The scope keyword argument describes whether the data requested is for a specific country, or for the world.
        Outputs:
        - Boolean var, if true, data is up to date.
        - File name where the requested data is stored."""
    for file in os.listdir(".\\data"):
        if file.endswith(".txt"):
            if file.split(".")[0] == str(datetime.date.fromtimestamp(time.time() - 30 * 3600)) + scope:
                print("Data is up to date!")
                return True, file
    print("Update is needed!")
    return False, None


def write_in_file(data, scope="world"):
    """ Writes the scrapped data to a text file.
        Arguments:
        - data (dict): the data to be stored in file.
        - scope (keyword, str): the scope of the data.
        No outputs"""

    # File name is the date 30 hrs ago (the site takes that much to update) and scope
    file = open(".\\data\\" + str(datetime.date.fromtimestamp(time.time() - 30 * 3600)) + scope + ".txt", "w")

    for key in data:
        file.write(key + "\n")
        if type(data[key]) == dict:
            for key2 in data[key]:
                file.write(key2 + "\n")
                file.write(str(data[key][key2]) + "\n")
        elif type(data[key]) == list:
            for val in data[key]:
                file.write(str(val) + "\n")
    return


def read_from_file(file):
    """ Read stored data.
        Arguments:
        - file (str): name of the file to be read.
        Outputs:
        - data (dict): the data read from the file."""

    # This is the structure of the data dictionary when empty
    data = {"demographics": {"population": None}, "cases": [],
            "deaths": [], "recovered": [], "active": []}
    f = open(".\\data\\" + file, "r")

    for line in f:
        line = line.rstrip()

        try:
            number = int(line)
        except ValueError:
            flag = line
            continue

        if flag == "population":
            data["demographics"]["population"] = number
        else:
            data[flag].append(number)
    return data


def demographic_data(scope="world"):
    """ Scraps demographic data from worldometers.
        Arguments:
        -scope (keyword, str)
        Outputs:
        -data (dataframe)"""

    # Data is scrapped from this site
    LINK = "https://www.worldometers.info/world-population/population-by-country/"
    response = requests.get(LINK)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.findAll("tbody")  # Finds the tables where data is extracted from
    rows = [i for i in table[0].findAll("tr")]
    data = []  # Data starts as a list

    for k in rows:
        elements = k.findAll("td")
        # Appends data for Country name, population, pop density, median age and urban %
        data.append({"Country": elements[1].find("a").contents[0],
                     "Population": int(elements[2].contents[0].replace(",","")),
                     "Density": elements[5].contents[0],
                     "Age": elements[9].contents[0],
                     "Urban": float(elements[11].contents[0][:-2])/100})

    # Packaged in a pandas dataframe, index is the Country name
    df_temp = pd.DataFrame(data)
    world_dem = df_temp.set_index("Country", drop=False)

    # Different scopes
    if scope == "world":
        data = world_dem
    # Make sure that the country your looking for is indexed correctly!
    # If it's not, make a special case for it.
    elif scope == "US":
        data = world_dem.loc(axis=0)["United States", "Population"]
    else:
        data = world_dem.loc(axis=0)[scope, "Population"]

    return data


def country_daily_data(country):
    """ Scraps daily data about Covid-19 total cases, active cases and deaths, from worldometers.
        Arguments:
            -country (str)
        Outputs:
            -cases (list): total Covid-19 cases reported in the country day by day.
            -deaths (list): total Covid-19 deaths reported in the country day by day.
            -active (list): total Covid-19 active cases reported in the country day by day."""

    # Make sure that the country arg matches the url of the country you're looking for.
    # If not, make a special case
    link = "https://www.worldometers.info/coronavirus/country/" + country
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

    # Makes the elements of the list ints
    cases = [int(i) for i in cases]
    deaths = [int(i) for i in deaths]
    active = [int(i) for i in active]

    # There are data from China from Jan 22nd, whereas other countries' data start from Feb 15th
    # To correct for the difference, extra zeroes are added when the country is not China, at the beginning of the list
    if country != "china":
        padding = [0 for i in range(24)]
        cases = padding + cases
        deaths = padding + deaths
        active = padding + active

    return cases, deaths, active


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
    cases = [int(i) for i in values]

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

    return cases, deaths, active


def mine_data(scope="world"):
    """ This function returns the data from the scope requested, in a format suitable for use by the model.
        Arguments:
            -scope (int): Either "world" or a specific country.
        Outputs:
            -data (dict)
    """

    # Is the file up to date?
    updated, file = up_to_date(scope=scope)

    # If not, scrap the new data.
    if not updated:
        print("Updating demographic data!")
        df_temp = demographic_data(scope=scope)

        # If the scope is the entire planet
        if scope == "world":
            world_popul = sum(df_temp.loc[:, "Population"])
            print("Updating global Covid-19 data!")
            cases, deaths, active_cases = world_daily_data()

            # This part calculates the total recovered cases day by day
            recov = []
            for i, val in enumerate(active_cases):
                recov.append(cases[i] - val)
            data = {"demographics": {"population": world_popul}, "cases": cases,
                    "deaths": deaths, "recovered": recov, "active": active_cases}

        # If the scope is a single country
        else:
            population = df_temp
            print("Updating country's Covid-19 data!")
            cases, deaths, active_cases = country_daily_data(scope.lower())

            # This part calculates the total recovered cases day by day
            recov = []
            for i, val in enumerate(active_cases):
                recov.append(cases[i] - val)
            data = {"demographics": {"population": population}, "cases": cases,
                    "deaths": deaths, "recovered": recov, "active": active_cases}
        # After scrapping, store the new data
        write_in_file(data, scope=scope)

    else:
        # Read the data from file if they are up to date.
        data = read_from_file(file)

    return data




