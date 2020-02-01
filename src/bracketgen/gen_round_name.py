import importdata.python_mysql_dbconf as db_conf
import mysql.connector


def read_round(tournament_name: str, iteration: str,
               detail1=None, detail2=None, detail3=None, league=False) -> list:
    """ Connect to MySQL database """

    db_config = db_conf.read_db_config()
    conn = None
    round_db = []

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            gen_conf = db_conf.read_general_config()
            if gen_conf["sql_output"] == "True":
                print('Importing round names from MySQL database')

        cursor = conn.cursor()

        if detail1 is None:  # only temporary matches have detail1 = "" which is ignored
            query_match = "SELECT detail1, detail2, detail3 FROM matches WHERE tournament_name=%s AND iteration=%s " \
                          "GROUP BY detail1, detail2, detail3"
            args_match = (tournament_name, iteration)
        else:
            if detail2 is None:
                if detail3 is None:
                    query_match = ("SELECT detail1, detail2, detail3 FROM matches WHERE tournament_name=%s "
                                   "AND iteration=%s AND detail1=%s "
                                   "GROUP BY detail2, detail3")
                    args_match = (tournament_name, iteration, detail1)
                else:
                    query_match = ("SELECT detail1, detail2, detail3 FROM matches WHERE tournament_name=%s "
                                   "AND iteration=%s AND detail1=%s AND detail3=%s"
                                   "GROUP BY detail2")
                    args_match = (tournament_name, iteration, detail1, detail3)
            else:
                if detail3 is None:
                    query_match = ("SELECT detail1, detail2, detail3 FROM matches WHERE tournament_name=%s "
                                   "AND iteration=%s AND detail1=%s AND detail2=%s"
                                   "GROUP BY detail3")
                    args_match = (tournament_name, iteration, detail1, detail2)
                else:
                    query_match = ""
                    args_match = ()
                    print("Specifying all 3 parameters is not allowed in this function")
                    exit(3)
        cursor.execute(query_match, args_match)

        total_rows = cursor.fetchall()
        for row in total_rows:
            result1 = row[0]
            result2 = row[1]
            result3 = row[2]
            result3 = '' if (len(result3) == 0 or result3.endswith('局')) else result3
            if detail1 is None:
                if round_db.count(result1 + result2 + result3) == 0:
                    round_db.append(result1 + result2 + result3)
            else:
                if detail2 is None:
                    if detail3 is None:
                        if round_db.count(result2 + result3) == 0:
                            round_db.append(result2 + result3)
                    else:
                        if round_db.count(result2) == 0:
                            round_db.append(result2)
                else:
                    if round_db.count(result3) == 0:
                        round_db.append(result3)
        cursor.close()

        conn.commit()

    except mysql.connector.Error as e:
        print(e)
    except Exception as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        round_db.sort(key=lambda x: round_name_value(x), reverse=not league)
        gen_conf = db_conf.read_general_config()
        if gen_conf["sql_output"] == "True":
            print(f"Reading Round data of {tournament_name} iteration {iteration}"
                  f" detail1:{detail1}, detail2:{detail2}, detail3:{detail3} complete")
        return round_db


def round_name_value(round_name: str):
    int_round_value = 0
    if round_name.endswith("回戦"):
        int_round_value = int(round_name[:2])
    elif round_name.endswith("準々決勝"):
        int_round_value = 98
    elif round_name.endswith("準決勝"):
        int_round_value = 99
    elif round_name.endswith("決勝"):
        int_round_value = 100
    elif round_name.endswith("番勝負"):
        int_round_value = 101
    return int_round_value
