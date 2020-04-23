######## Imports #######
import requests
import time
from bs4 import BeautifulSoup
import pandas
import re
import numpy
import matplotlib
import tkinter
import matplotlib.pyplot
import lxml
from lxml import etree
import datetime
import os
import sys


## Function to separate the elements of a table and return them row-by-row
def take_information(rows):

## list_rows is the list with all elements sorted by country
    list_rows = []
    for x in rows:
        new_rows = [i for i in x.findAll("td")]
        list_rows.append(new_rows)
    count = 0

    for x in list_rows:
        list_rows[count] = x[1:]
        count += 1
    counter = 0

    for x in list_rows:
        count = 0
        for y in x:
            y = str(y).split('<')[1:]
            coun = 0
            for z in y:
                y[coun] = z.split('>')[1:]
                coun += 1
            for z in y:
                if z != ['']:
                    y = z
            x[count] = str(y).replace("['", '').replace("']", "")
            if count == 0:
                x[count] = x[count].replace("&amp;", "and")
            count += 1
        list_rows[counter] = x
        counter += 1
    return list_rows


def create_dictionary(list_rows):

## Creating a dictionary to save all the information we collect (we need)
    counter = len(list_rows[0])
    dictionary1 = {}

## Function to separate the common elements in order to add and categorize them in dictionary
    for x in range(counter):
        dictionary1.update({str(x): []})
        for i in list_rows:
            dictionary1[str(x)].append(i[x])
    return dictionary1


## Definition of our sources (we must save them in a dictionary or ask from user)
source = "https://www.worldometers.info/world-population/population-by-country/"
data = requests.get(source).text
soup = BeautifulSoup(data, 'lxml')
article = soup.find('article')
#print(soup.pretify())


## Extracting the table we want to edit
table = soup.findAll("tbody")  # Finds the tables where data is extracted from
rows = [i for i in table[0].findAll("tr")]
data = []  # Data starts as a list


## Taking our information for all the countries in site organized in rows (lists)
list_rows = take_information(rows)

dictionary = create_dictionary(list_rows)
#print(dictionary)

organized_data = pandas.DataFrame(data = dictionary)
print(organized_data)



#fig, axs = matplotlib.pyplot.subplots(7, 1, sharex = True)

#axs[0].plot(list1[0])
#axs[1].plot(list1[1])
#axs[2].plot(list1[2])
#axs[3].plot(list1[3])
#axs[4].plot(list1[4])
#axs[5].plot(list1[5])
#axs[6].plot(list1[6])

#matplotlib.pyplot.show()


#doc.find(text = "INSERT FOOTER HERE").replace_with(footer)