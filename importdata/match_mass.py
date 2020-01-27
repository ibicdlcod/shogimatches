from importdata import match_auto

dict_tour_name = {"ryuou": 1, "meijin": 2, "junni": 3, "eiou": 12,
                  "oui": 4, "ouza": 5, "kiou": 6, "oushou": 7,
                  "kisen": 8}

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