from importdata import match_auto

RYUOU = 1

if __name__ == '__main__':
    match_list = []
    for i in range(1, 33):
        match_list.append(match_auto.import_data(i, 1))
    match_auto.match_to_sql(match_list)