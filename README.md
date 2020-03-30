# Coronavirus-Basic-Model

A basic mathematical tool for predicting the spread of the Covid-19 pandemic, using the SIR model for infectious
diseases. It was created by Chistos Frantzolas and Ilias Xenogiannis.
This project can run with versions of Python above 3.5.2. You can install the complete requirements by using the
command 'pip install -r requirements.txt'. [a]

**Disclaimer:** Neither I nor anyone that currently works on this project is an epidimiologist.
This project has been built for purely academic purposes.

## SIR Model

Compartmental models are a technique used to simplify the mathematical modelling of infectious disease. The population is divided into compartments, with the assumption that every individual in the same compartment has the same characteristics. [1]

The SIR model divides the population into 3 groups:
S = S(t)	is the number of susceptible individuals,
I = I(t)	is the number of infected/infectious individuals, and
R = R(t)	is the number of recovered/removed individuals. [2]

We make the assumptions that:
1. No one is added to the susceptible group, since we are ignoring births and immigration.
2. The time-rate of change of  S(t),  the number of susceptibles depends on the number already susceptible, the number of individuals already infected, and the amount of contact between susceptibles and infecteds. In particular, suppose that each infected individual has a fixed number  b  of contacts per day that are sufficient to spread the disease.
3. We also assume that a fixed fraction  k  of the infected group will recover during any given day. [2]

The differential equations that describe the model are as follows: [1]

![Image of Diff Equations](https://wikimedia.org/api/rest_v1/media/math/render/svg/29728a7d4bebe8197dca7d873d81b9dce954522e)

You can find more information about the SIR model in the resources [3], [4].

Note that there are 2 parameters we don't know the values of (β, γ, presented as b and k in the code respectively). We can estimate the number of days each person remain infectious and thus have the recovery rate be the inverse of this period. On the other hand, there are studies on the R0 (basic reproductive rate) of the novel coronavirus, which is the number of people an infectious person is going to transmit the virus to in total. The R0 of Covid-19 is estimated to be 2.06 to 2.52. [5] Then, we can calculate b, with the equation:

![Image of R0 equation](https://wikimedia.org/api/rest_v1/media/math/render/svg/4aae42f8253a395c52a798a9ad5a7e4adb6fceea)

Of course, b is not going to remain constant. Preventative measures like social distancing, lockdowns and better hygiene limit possible contacts that end up transmitting the virus, thus reducing b. On the other hand, environmental factors can also have an impact on the transmission rate of an infectious disease, although it's not yet certain how this will affect the Covid-19 epidemic.

## Scrapping Data

The population data and the Covid-19 confirmed cases and deaths data is taken from Worldometers.

More specifically, the population data by country, along with data for age, urbanization, density etc. are taken from [6].
The total confirmed cases of Coronavirus for the entire planet is taken from the "Total Cases" graph on [7], the daily total death toll from the "Total Deaths" graph on [8] and the active cases day-by-day are taken from the "Active Cases" graph on [9].
Finally, data for each specific country is taken from their respective graphs in each country's page, if there is one. p.e. China [10]

The graphs on the site is updated approximately every 24 hours. Thus, if the model runs a scenario it hasn't run in the last 30 hours it will update its data base (simple text files for the time being). In any other case, it will simply read data from the corresponding files.

In order to understand the scrapping function you need to know some basic things about the regular expressions module of Python 3 [b]

## Running the Model


## Ideas for the Future

As the project is in its very early stages, there is much room for improvement. You can contribute to it by:
1. Improving the data collection or expanding it through other sources to encompass things like:
   1. Measures taken by governments.
   1. Hospital capacity in each country.
   1. Deviding populations by groups.
   1. Testing numbers.
   1. Dividing countries into smaller areas.
1. Improving the model itself:
   1. Figure out different trends in the data.
   1. Calculate the transmission rate in different conditions (climate, measures etc.)
   1. Use different models to simulate the effects of different preventative measures.
1. Improving the presentation of the simulation.
   1. Create an animation through time.
   1. Make maps that demonstrate the spread of the disease.
1. And anything else that comes to mind!

## FAQ


## Sources

1. https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
2. https://www.maa.org/press/periodicals/loci/joma/the-sir-model-for-spread-of-disease-the-differential-equation-model
3. https://www.youtube.com/watch?v=k6nLfCbAzgo
4. https://www.youtube.com/watch?v=gxAaO2rsdIs
5. https://www.ijidonline.com/article/S1201-9712(20)30091-6/fulltext
6. https://www.worldometers.info/world-population/population-by-country/
7. https://www.worldometers.info/coronavirus/
8. https://www.worldometers.info/coronavirus/coronavirus-death-toll/
9. https://www.worldometers.info/coronavirus/coronavirus-cases/
10. https://www.worldometers.info/coronavirus/country/china/

### Extra

a. https://pip.pypa.io/en/latest/user_guide/#requirements-files
b. https://docs.python.org/3/library/re.html
