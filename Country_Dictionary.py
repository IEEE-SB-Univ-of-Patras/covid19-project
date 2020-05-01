""" This file draws the names of the selected countries and the url-codes of them
    from two different files with certain allignment and creates a dictionary with them.
     <key: value = name: code>
     Also, it creates a file with the info provided by the dictionary like:
     (key:value\n) """


def country_dictionary_creator(country_names, country_urls):
    """
    This Function creates a dictionary with keys the names of the countries and urls as values.
    The names and the urls are written in 2 different .txt files.

    :param country_names:(string) the filename.txt of the file where country names are.
    :param country_urls: (string) the filename.txt of the file where country urls are.
    :return: a dictionary: (dictionary) key:value = name:url
    """

    country_dict = {}
    country_url_list = []

    # Read from files
    with open(country_names, "r") as file_country_names:
        for line in file_country_names:
            country_name = line.strip()
            country_dict[country_name] = " "

    with open(country_urls, "r") as file_country_urls:
        for line in file_country_urls:
            country_url = line.strip()
            country_url_list.append(country_url)

    # Dictionary Creation
    i = 0
    for key in country_dict.keys():
        country_dict[key] = country_url_list[i]
        i += 1

    file_country_names.close()
    file_country_urls.close()

    return country_dict


def write_dictionary_file(country_dictionary):
    """
    This function writes the keys and the values of the dictionary where names and codes are in a file:
    (name:code\n).
    :param country_dictionary: (dictionary) The dictionary where the names and the codes of the countries are.
                                key:value = name:url
    :return: (int) 0
    """

    country_file = open("country_names_urls.txt", "w")
    for key in country_dictionary.keys():
        country_file.write(str(key) + ":" + str(country_dictionary[key]) + "\n")

    country_file.close()

    return 0


def country_link_creator(country_dictionary, key_country):
    """
    This function creates the link for scrapping of a selected country
    :param country_dictionary: (dictionary) A dictionary where key:value = name:code
    :param key_country: (string) The selected country
    :return: (string) the link for scrapping
    """
    country_url = "https://www.worldometers.info/coronavirus/country/"

    return country_url + country_dictionary[key_country]


def debug_country_dictionary_creator(country_file, country_dict):
    """
    JUST FOR DEBUGGING: Creates a new dictionary from the file created from write_dictionary_file() function.
    :param country_file: (string) The name of the file.txt
    :param country_dict: (dictionary) The dictionary with the names and codes of the countries
    :return: (dictionary) new dictionary with names and codes
    """

    with open(country_file, "r") as file_country:
        for line in file_country:
            country_info = line.strip().split(":")

            country_dict[country_info[0]] = country_info[1]

    return country_dict


def main():

    country_dictionary = {}
    debug_dictionary = {}
    country_name_file = "country_names.txt"
    country_code_file = "country_codes.txt"

    country_dictionary = country_dictionary_creator(country_name_file, country_code_file)
    print(country_dictionary)

    write_dictionary_file(country_dictionary)
    print(debug_country_dictionary_creator("country_names_urls.txt", debug_dictionary))


if __name__ == "__main__":
    main()
