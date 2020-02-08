from importdata import match_auto
from configparser import ConfigParser
import os

dict_tour_name = {"ryuou": 1, "meijin": 2, "junni": 3, "eiou": 12, "oui": 4,
                  "ouza": 5, "kiou": 6, "oushou": 7, "kisei": 8, "asahi_cup": 9,
                  "ginga": 10, "nhk": 11, "jt": 13, "shinjin": 14, "kakogawa": 15,
                  "yamada": 34, "dan10": 17, "dan9": 35, "meijin_dan9": 36, "meiki": 20,
                  "seirei": 101, "mynavi": 102, "jo_ouza": 103, "jo_meijin": 104, "jo_oui": 105,
                  "jo_oushou": 106, "touka": 107, "jo_yamada": 108}


def read_mass_config(filename: str = 'config\\match_mass.ini',
                     section: str = 'match_mass') -> dict:
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        print(os.getcwd())
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


def match_mass():
    conf0 = read_mass_config('config\\match_mass.ini', 'general')
    if conf0["enabled"] != "True":
        return
    conf = read_mass_config()

    if conf["ryuou"] == "True":
        for i in range(1, 33):
            match_list = match_auto.import_data(i, dict_tour_name["ryuou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 1 with iteration {i} succeeded")
    if conf["meijin"] == "True":
        for i in range(13, 78):
            match_list = match_auto.import_data(i, dict_tour_name["meijin"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 2 with iteration {i} succeeded")
    if conf["junni"] == "True":
        for i in range(8, 78):
            if i in range(31, 36):
                continue
            match_list = match_auto.import_data(i, dict_tour_name["junni"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 3 with iteration {i} succeeded")
    if conf["eiou"] == "True":
        for i in range(3, 5):
            match_list = match_auto.import_data(i, dict_tour_name["eiou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 12 with iteration {i} succeeded")
        for i in range(1001, 1003):  # 2001-2002
            match_list = match_auto.import_data(i, dict_tour_name["eiou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 12 with iteration {i} succeeded")
    if conf["oui"] == "True":
        for i in range(1, 61):
            match_list = match_auto.import_data(i, dict_tour_name["oui"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 4 with iteration {i} succeeded")

    if conf["ouza"] == "True":
        for i in range(31, 68):
            match_list = match_auto.import_data(i, dict_tour_name["ouza"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 5 with iteration {i} succeeded")
        for i in range(1002, 1031):
            match_list = match_auto.import_data(i, dict_tour_name["ouza"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 5 with iteration {i} succeeded")
    if conf["kiou"] == "True":
        for i in range(1, 46):
            match_list = match_auto.import_data(i, dict_tour_name["kiou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 6 with iteration {i} succeeded")
        for i in range(1001, 1002):
            match_list = match_auto.import_data(i, dict_tour_name["kiou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 6 with iteration {i} succeeded")
    if conf["oushou"] == "True":
        for i in range(3, 69):
            match_list = match_auto.import_data(i, dict_tour_name["oushou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 7 with iteration {i} succeeded")
    if conf["kisei"] == "True":
        for i in range(1, 91):
            match_list = match_auto.import_data(i, dict_tour_name["kisei"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 8 with iteration {i} succeeded")
    if conf["asahi_cup"] == "True":
        for i in range(1001, 1013):
            match_list = match_auto.import_data(i, dict_tour_name["asahi_cup"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 9 with iteration {i} succeeded")

    if conf["ginga"] == "True":
        for i in range(1008, 1028):
            match_list = match_auto.import_data(i, dict_tour_name["ginga"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 10 with iteration {i} succeeded")
    if conf["nhk"] == "True":
        for i in range(1003, 1069):
            match_list = match_auto.import_data(i, dict_tour_name["nhk"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 11 with iteration {i} succeeded")
    if conf["jt"] == "True":
        for i in range(1001, 1041):
            match_list = match_auto.import_data(i, dict_tour_name["jt"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 13 with iteration {i} succeeded")
    if conf["shinjin"] == "True":
        for i in range(1001, 1051):
            match_list = match_auto.import_data(i, dict_tour_name["shinjin"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 14 with iteration {i} succeeded")
    if conf["kakogawa"] == "True":
        for i in range(1001, 1010):
            match_list = match_auto.import_data(i, dict_tour_name["kakogawa"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 15 with iteration {i} succeeded")

    if conf["yamada"] == "True":
        for i in range(1001, 1005):
            match_list = match_auto.import_data(i, dict_tour_name["yamada"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 34 with iteration {i} succeeded")
    if conf["dan10"] == "True":
        for i in range(1, 27):
            match_list = match_auto.import_data(i, dict_tour_name["dan10"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 17 with iteration {i} succeeded")
    if conf["dan9"] == "True":
        for i in range(4, 13):
            match_list = match_auto.import_data(i, dict_tour_name["dan9"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 35 with iteration {i} succeeded")
    if conf["meijin_dan9"] == "True":
        for i in range(1006, 1009):
            match_list = match_auto.import_data(i, dict_tour_name["meijin_dan9"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 36 with iteration {i} succeeded")
    if conf["meiki"] == "True":
        for i in range(1003, 1008):
            match_list = match_auto.import_data(i, dict_tour_name["meiki"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 20 with iteration {i} succeeded")
        for i in range(1, 4):
            match_list = match_auto.import_data(i, dict_tour_name["meiki"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 20 with iteration {i} succeeded")

    if conf["seirei"] == "True":
        for i in range(1, 2):
            match_list = match_auto.import_data(i, dict_tour_name["seirei"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 101 with iteration {i} succeeded")
    if conf["mynavi"] == "True":
        for i in range(1, 13):
            match_list = match_auto.import_data(i, dict_tour_name["mynavi"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 102 with iteration {i} succeeded")
    if conf["jo_ouza"] == "True":
        for i in range(1, 10):
            match_list = match_auto.import_data(i, dict_tour_name["jo_ouza"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 103 with iteration {i} succeeded")
    if conf["jo_meijin"] == "True":
        for i in range(1, 47):
            match_list = match_auto.import_data(i, dict_tour_name["jo_meijin"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 104 with iteration {i} succeeded")
    if conf["jo_oui"] == "True":
        for i in range(1, 31):
            match_list = match_auto.import_data(i, dict_tour_name["jo_oui"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 105 with iteration {i} succeeded")

    if conf["jo_oushou"] == "True":
        for i in range(1, 42):
            match_list = match_auto.import_data(i, dict_tour_name["jo_oushou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 106 with iteration {i} succeeded")
    if conf["touka"] == "True":
        for i in range(1, 28):
            match_list = match_auto.import_data(i, dict_tour_name["touka"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 107 with iteration {i} succeeded")
    if conf["jo_yamada"] == "True":
        for i in range(1, 6):
            match_list = match_auto.import_data(i, dict_tour_name["jo_yamada"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 108 with iteration {i} succeeded")
