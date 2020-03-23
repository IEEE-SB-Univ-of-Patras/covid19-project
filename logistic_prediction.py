""" Try to predict the spread of the Coronavirus.
    Perfect your model, collect data, or present your
    simulation in new ways."""

# Imports
import datetime
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Global Variables
""" Source of data: https://www.worldometers.info/coronavirus/"""
CASES_NOW = 304622
CASES_TODAY = 31000
DEATHS_NOW = 13000

# Current date
NOW = datetime.date.today()

# Population of simulation
POPULATION = 7.79 * 10**9  # Here, it is the population of the entire planet


def exponential_growth(days=180, limit=0.5, growth_factor=1.12, death_rate=0.041):
    """ This function simulates the spread of the virus using a simple logistic curve.
        https://en.wikipedia.org/wiki/Logistic_function.
        The function takes the following keyword arguments:
        - days (int, default 100): The duration of the projection in days.
        - limit (float, default 0.5): The percentage of the population infected in the end. It should be
                                      between 0.0 and 1.0.
        - growth_factor (float, default 1.12): The increase in new cases from the previous day, on average.
          https://www.worldometers.info/coronavirus/coronavirus-cases/#cases-growth-factor
        - death_rate (float, default 0.05): The number of deaths divided by the number of total cases.
        The function outputs:
        - date_list (list of datetime objects): The dates in which the simulation takes place.
        - today_list (list of ints): The number of new cases each day.
        - cases_list (list of ints): The number of total cases each day.
        - death_list (list of ints): The number of total deaths each day."""

    # Initializing variables
    cases = CASES_NOW
    today = CASES_TODAY
    deaths = DEATHS_NOW
    date = NOW
    date_list = [date]
    today_list = [today]
    cases_list = [cases]
    deaths_list = [deaths]
    cases_limit = limit * POPULATION  # The maximum number of cases each day.

    for i in range(days):
        # Looping through the days of the simulation, calculating new cases.

        '''The amount of people the virus can infect is not infinite. The more people are infected,
           the less people are there to be infected, so the growth factor of new cases starts falling.
           By the point the virus has burned through half the available people, the growth factor starts falling
           below 1, and daily cases start falling until they reach zero. The pandemic is over almost as
           fast as it began. That is, if the virus is left to take its course with no measures.'''

        # Calculating the date i + 1 days after today
        date = datetime.date.fromtimestamp(time.time() + (i + 1) * 24 * 3600)
        date_list.append(date)

        growth = growth_factor - 1
        # This day's growth factor, 1 when the virus infect half the cases_limit
        growth_factor_ = 1 + growth * (1 - 2 * cases / cases_limit)

        # New cases
        today = int(today*growth_factor_)
        today_list.append(today)

        # Increasing the total number of cases.
        cases += today
        cases_list.append(cases)

        # The death rate is assumed to be stable
        deaths = int(cases * death_rate)
        deaths_list.append(deaths)

        # Printing each days information
        print(str(date) + ": " + str(format(today, ',d')) + " new cases and "
              + str(format(cases, ',d')) + " total cases and "
              + str(format(deaths, ',d')) + " deaths.")

    return date_list, today_list, cases_list, deaths_list


def plotting(dates, todays, cases, deaths):
    """ This function plots the number of new daily cases, total cases,
        and total deaths against time elapsed in the simulation, using
        matplotlib."""
    t = np.array(dates)
    c = np.array(cases)
    d = np.array(deaths)
    to = np.array(todays)

    fig, ax = plt.subplots()
    plt.yscale("log")
    ax.plot(t, c)
    ax.plot(t, d)
    ax.plot(t, to)

    ax.set(xlabel='Days', ylabel='Cases',
           title='Flatten the curve, folks')
    ax.grid()

    # fig.savefig("test.png")
    plt.show()


dates, todays, cases, deaths = exponential_growth(death_rate=DEATHS_NOW/CASES_NOW)
plotting(dates, todays, cases, deaths)
