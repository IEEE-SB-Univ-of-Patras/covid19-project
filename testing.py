import pandas as pd
import csv
import urllib
import requests
import os
from io import StringIO
import time
from selenium import webdriver
import time
from time import gmtime, strftime


mylasttime = int(str(gmtime()).split(", ")[3].strip("tm_hour="))

while True:

    print(str(gmtime()).split(", ")[3], str(gmtime()).split(", ")[4], str(gmtime()).split(", ")[5])
    mytime = int(str(gmtime()).split(", ")[3].strip("tm_hour="))

    if mytime != mylasttime:

        try:#σε περιπτωση σφαλματος

            url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

            source = requests.get(url, allow_redirects=True)
            StringData = StringIO(source.text)
            data = pd.read_csv(StringData)[["date", "location", "iso_code", "total_tests", "new_tests"]]
            data.rename(columns={"date": "Date", "location": "Country", "iso_code": "Country_code", "total_tests": "Total_tests", "new_tests": "New_tests"})

            time.sleep(1)

            print(data)

        except: print("ohh fuck")

        mylasttime = mytime
        time.sleep(43919)#χρονος για να καθυστερει μια μερα
        #ωστε αν τρεχει συνεχομενα το προγραμμα να κατεβασει ξανα σε μια μερα
        #μπορει να κατεβαζει και ανα ωρα αν το φτιαξουμε

    time.sleep(20)
