import Country_Dictionary as cd
import pandas as pd


def keep():
    worldometers_dictionary = {}
    cd.debug_country_dictionary_creator("countries_worldometers.txt", worldometers_dictionary)
    print(worldometers_dictionary)

    mobility_dictionary = {}
    cd.debug_country_dictionary_creator("countries_mobility.txt", mobility_dictionary)
    print(mobility_dictionary)

    measures_dictionary = {}
    cd.debug_country_dictionary_creator("countries_measures.txt", measures_dictionary)
    print(measures_dictionary)


if __name__ == "__main__":
    keep()
