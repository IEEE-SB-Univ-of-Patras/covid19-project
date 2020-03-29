# Coronavirus-Basic-Model

A basic mathematical tool for predicting the spread of the Covid-19 pandemic, using the SIR model for infectious
diseases. It was created by @Frankkie and @ilias1111
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

## Scrapping Data


## Running the Model


## Ideas for the Future


## FAQ


## Sources

1. https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
2. https://www.maa.org/press/periodicals/loci/joma/the-sir-model-for-spread-of-disease-the-differential-equation-model
3. https://www.youtube.com/watch?v=k6nLfCbAzgo
4. https://www.youtube.com/watch?v=gxAaO2rsdIs

### Extra

a. https://pip.pypa.io/en/latest/user_guide/#requirements-files
