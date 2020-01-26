from importdata import match_auto

RYUOU = 1

if __name__ == '__main__':
    match_list = []
    for i in range(5, 33):
        match_list = match_auto.import_data(i, 1)
        match_auto.match_to_sql(match_list)
        print(f"Retrieving web information for tournament 1 with iteration {i} succeeded")
