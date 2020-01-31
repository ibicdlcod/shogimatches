from datetime import date
from importdata import sql_read
import importdata.python_mysql_dbconf as db_conf
import mysql.connector


def to_sql(in_iteration: int, winner_name: str, tournament_name: str, in_date: date) -> None:
    db_config = db_conf.read_db_config()
    conn = None

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        cursor = conn.cursor()
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        query_insert = ("INSERT INTO former(tournament_name, iteration_int, end_date, winner_fullname)\n"
                        "VALUES(%s,%s,%s,%s)\n"
                        "ON DUPLICATE KEY UPDATE winner_fullname = VALUES(winner_fullname);")
        args_insert = (tournament_name, in_iteration, in_date.isoformat(), winner_name)
        cursor = conn.cursor()
        cursor.execute(query_insert, args_insert)

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
    pass


def from_sql(in_id: int, tournament_name: str):
    db_config = db_conf.read_db_config()
    conn = None
    result = None

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        cursor = conn.cursor(buffered=True)
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        query_insert = ("SELECT * FROM former\n"
                        "WHERE iteration_int=%s AND tournament_name=%s;\n")
        args_insert = (in_id, tournament_name)
        cursor = conn.cursor()
        cursor.execute(query_insert, args_insert)
        row = cursor.fetchall()
        if row is None:
            pass
        else:
            result = row[0]

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return result


ryuou_end_dates = dict()
ryuou_end_dates[0] = date.fromisoformat("1900-10-01")
ryuou_winners = {0: None}
meijin_end_dates = dict()
meijin_end_dates[12] = date.fromisoformat("1901-04-01")
meijin_winners = {12: None}

gen_conf = db_conf.read_general_config()
if gen_conf["renew_former_table"] == "True":
    print('Renew former meijin/ryuou table')
    for i in range(1, 9):
        iteration = "第" + str(i).zfill(2) + "期"
        ryuou_matches = sql_read.read_match("竜王戦", iteration, "タイトル戦", "七番勝負")
        ryuou_matches.sort(key=lambda x: x.match_date)
        end_date = ryuou_matches[-1].match_date
        ryuou_end_dates[i] = end_date
        ryuou_winners[i] = (ryuou_matches[-1].black_name if ryuou_matches[-1].win_loss_for_black > 0
                            else ryuou_matches[-1].white_name)
    ryuou_end_dates[9] = date.fromisoformat("2099-10-01")
    ryuou_winners[7] = None
    ryuou_winners[8] = None
    ryuou_winners[9] = None
    for i in range(0, 10):
        to_sql(i, ryuou_winners[i], "竜王戦", ryuou_end_dates[i])

    for i in range(13, 54):
        iteration = "第" + str(i).zfill(2) + "期"
        meijin_matches = sql_read.read_match("名人戦", iteration, "タイトル戦", "七番勝負")
        meijin_matches.sort(key=lambda x: x.match_date)
        end_date = meijin_matches[-1].match_date
        meijin_end_dates[i] = end_date
        meijin_winners[i] = (meijin_matches[-1].black_name if meijin_matches[-1].win_loss_for_black > 0
                             else meijin_matches[-1].white_name)
    meijin_end_dates[54] = date.fromisoformat("2099-04-01")
    meijin_winners[52] = None
    meijin_winners[53] = None
    meijin_winners[54] = None
    for i in range(12, 55):
        to_sql(i, meijin_winners[i], "名人戦", meijin_end_dates[i])
else:
    for i in range(0, 10):
        result_i = from_sql(i, "竜王戦")
        ryuou_end_dates[i] = result_i[2]
        ryuou_winners[i] = result_i[3]
    for j in range(12, 55):
        result_j = from_sql(j, "名人戦")
        meijin_end_dates[j] = result_j[2]
        meijin_winners[j] = result_j[3]


def import_former_ryuou(in_date: date = date.fromisoformat("1900-01-01")):
    current_ryuou_iteration = 0
    while in_date >= ryuou_end_dates[current_ryuou_iteration + 1]:
        current_ryuou_iteration += 1
    former_ryuou_iteration = current_ryuou_iteration - 1
    if former_ryuou_iteration <= 0:
        return None
    else:
        return ryuou_winners[former_ryuou_iteration]
    

def import_former_meijin(in_date: date = date.fromisoformat("1900-01-01")):
    current_meijin_iteration = 11
    while in_date >= meijin_end_dates[current_meijin_iteration + 1]:
        current_meijin_iteration += 1
    former_meijin_iteration = current_meijin_iteration - 1
    if former_meijin_iteration <= 12:
        return None
    else:
        return meijin_winners[former_meijin_iteration]
