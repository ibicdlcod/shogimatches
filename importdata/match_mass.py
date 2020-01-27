from importdata import match_auto

dict_tour_name = {"ryuou": 1, "meijin": 2, "junni": 3, "eiou": 12, "oui": 4,
                  "ouza": 5, "kiou": 6, "oushou": 7, "kisei": 8, "asahi_cup": 9,
                  "ginga": 10, "nhk": 11, "jt": 13, "shinjin": 14, "kakogawa": 15,
                  "yamada": 34, "dan10": 17, "dan9": 35}

if __name__ == '__main__':
    match_list = []
    ryuou = False
    meijin = False
    junni = False
    eiou = False
    oui = False

    if ryuou:
        for i in range(1, 33):
            match_list = match_auto.import_data(i, dict_tour_name["ryuou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 1 with iteration {i} succeeded")
    if meijin:
        for i in range(13, 78):
            match_list = match_auto.import_data(i, dict_tour_name["meijin"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 2 with iteration {i} succeeded")
    if junni:
        for i in range(8, 78):
            if i in range(31, 36):
                continue
            match_list = match_auto.import_data(i, dict_tour_name["junni"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 3 with iteration {i} succeeded")
    if eiou:
        for i in range(3, 5):
            match_list = match_auto.import_data(i, dict_tour_name["eiou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 12 with iteration {i} succeeded")
        for i in range(1001, 1003):  # 2001-2002
            match_list = match_auto.import_data(i, dict_tour_name["eiou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 12 with iteration {i} succeeded")
    if oui:
        for i in range(1, 61):
            match_list = match_auto.import_data(i, dict_tour_name["oui"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 4 with iteration {i} succeeded")

    ouza = False
    kiou = False
    oushou = False
    kisei = False
    asahi_cup = False
    if ouza:
        for i in range(31, 68):
            match_list = match_auto.import_data(i, dict_tour_name["ouza"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 5 with iteration {i} succeeded")
        for i in range(1002, 1031):
            match_list = match_auto.import_data(i, dict_tour_name["ouza"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 5 with iteration {i} succeeded")
    if kiou:
        for i in range(1, 46):
            match_list = match_auto.import_data(i, dict_tour_name["kiou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 6 with iteration {i} succeeded")
        for i in range(1001, 1002):
            match_list = match_auto.import_data(i, dict_tour_name["kiou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 6 with iteration {i} succeeded")
    if oushou:
        for i in range(3, 69):
            match_list = match_auto.import_data(i, dict_tour_name["oushou"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 7 with iteration {i} succeeded")
    if kisei:
        for i in range(1, 91):
            match_list = match_auto.import_data(i, dict_tour_name["kisei"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 8 with iteration {i} succeeded")
    if asahi_cup:
        for i in range(1001, 1013):
            match_list = match_auto.import_data(i, dict_tour_name["asahi_cup"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 9 with iteration {i} succeeded")

    ginga = False
    nhk = False
    jt = False
    shinjin = False
    kakogawa = False
    if ginga:
        for i in range(1008, 1028):
            match_list = match_auto.import_data(i, dict_tour_name["ginga"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 10 with iteration {i} succeeded")
    if nhk:
        for i in range(1003, 1069):
            match_list = match_auto.import_data(i, dict_tour_name["nhk"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 11 with iteration {i} succeeded")
    if jt:
        for i in range(1001, 1041):
            match_list = match_auto.import_data(i, dict_tour_name["jt"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 13 with iteration {i} succeeded")
    if shinjin:
        for i in range(1001, 1051):
            match_list = match_auto.import_data(i, dict_tour_name["shinjin"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 14 with iteration {i} succeeded")
    if kakogawa:
        for i in range(1001, 1010):
            match_list = match_auto.import_data(i, dict_tour_name["kakogawa"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 15 with iteration {i} succeeded")

    yamada = False
    dan10 = False
    dan9 = True
    if yamada:
        for i in range(1001, 1005):
            match_list = match_auto.import_data(i, dict_tour_name["yamada"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 34 with iteration {i} succeeded")
    if dan10:
        for i in range(1, 27):
            match_list = match_auto.import_data(i, dict_tour_name["dan10"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 17 with iteration {i} succeeded")
    if dan9:
        for i in range(4, 13):
            match_list = match_auto.import_data(i, dict_tour_name["dan9"])
            match_auto.match_to_sql(match_list)
            print(f"Retrieving web information for tournament 35 with iteration {i} succeeded")