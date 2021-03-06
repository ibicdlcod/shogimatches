from metastruct import kishi_data, match_data
import importdata.python_mysql_dbconf as db_conf
import mysql.connector


def read_kishi() -> list:
    """ Connect to MySQL database """

    db_config = db_conf.read_db_config()
    conn = None
    kishi_db = []

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            gen_conf = db_conf.read_general_config()
            if gen_conf["sql_output"] == "True":
                print('Importing Kishi from MySQL database')

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM kishi")

        row = cursor.fetchone()
        while row is not None:
            current_kishi: kishi_data.Kishi = kishi_data.Kishi(
                row[0], row[1], row[2], row[3], row[4] == 1,
                row[5] == 1, row[6] == 1
            )
            kishi_db.append(current_kishi)
            row = cursor.fetchone()
        cursor.close()

        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        kishi_db.sort(key=lambda x: x.id)
        gen_conf = db_conf.read_general_config()
        if gen_conf["sql_output"] == "True":
            print("Reading Kishi data complete")
        return kishi_db


def read_match(tournament_name: str, iteration: str,
               detail1=None, detail2=None, detail3=None) -> list:
    """ Connect to MySQL database """

    db_config = db_conf.read_db_config()
    conn = None
    match_db = []

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            gen_conf = db_conf.read_general_config()
            if gen_conf["sql_output"] == "True":
                print('Importing match from MySQL database')

        cursor = conn.cursor()
        if detail1 is None:  # only temporary matches have detail1 = "" which is ignored
            query_match = "SELECT * FROM matches WHERE tournament_name=%s AND iteration=%s"
            args_match = (tournament_name, iteration)
        else:
            if detail2 is None:
                if detail3 is None:
                    query_match = ("SELECT * FROM matches WHERE tournament_name=%s "
                                   "AND iteration=%s AND detail1=%s")
                    args_match = (tournament_name, iteration, detail1)
                else:
                    query_match = ("SELECT * FROM matches WHERE tournament_name=%s "
                                   "AND iteration=%s AND detail1=%s AND detail3=%s")
                    args_match = (tournament_name, iteration, detail1, detail3)
            else:
                if detail3 is None:
                    query_match = ("SELECT * FROM matches WHERE tournament_name=%s "
                                   "AND iteration=%s AND detail1=%s AND detail2=%s")
                    args_match = (tournament_name, iteration, detail1, detail2)
                else:
                    query_match = ("SELECT * FROM matches WHERE tournament_name=%s "
                                   "AND iteration=%s AND detail1=%s AND detail2=%s AND detail3=%s")
                    args_match = (tournament_name, iteration, detail1, detail2, detail3)
        cursor.execute(query_match, args_match)

        row = cursor.fetchone()
        while row is not None:
            current_match: match_data.Match = match_data.Match(
                row[1], row[2], row[3], row[4] == 1,
                row[5], row[6], row[7], row[8],
                row[9], row[10], row[11], row[12], row[13]
            )
            match_db.append(current_match)
            row = cursor.fetchone()
        cursor.close()

        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        match_db.sort(key=lambda x: x.match_date)
        gen_conf = db_conf.read_general_config()
        if gen_conf["sql_output"] == "True":
            print(f"Reading Match data of {tournament_name} iteration {iteration}"
                  f" detail1:{detail1}, detail2:{detail2}, detail3:{detail3} complete")
        return match_db


def read_match_min_max_date(tournament_name: str, iteration: str, min_or_max: str,
                            detail1=None, detail2=None, detail3=None) -> list:
    """ Connect to MySQL database """

    db_config = db_conf.read_db_config()
    conn = None
    result = []

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            gen_conf = db_conf.read_general_config()
            if gen_conf["sql_output"] == "True":
                print('Importing match from MySQL database')

        cursor = conn.cursor()
        if detail1 is None:  # only temporary matches have detail1 = "" which is ignored
            query_match = f"SELECT {min_or_max}(match_date) FROM matches WHERE tournament_name=%s AND iteration=%s"
            args_match = (tournament_name, iteration)
        else:
            if detail2 is None:
                if detail3 is None:
                    query_match = (f"SELECT {min_or_max}(match_date) FROM matches WHERE tournament_name=%s "
                                   "AND iteration=%s AND detail1=%s")
                    args_match = (tournament_name, iteration, detail1)
                else:
                    query_match = (f"SELECT {min_or_max}(match_date) FROM matches WHERE tournament_name=%s "
                                   "AND iteration=%s AND detail1=%s AND detail3=%s")
                    args_match = (tournament_name, iteration, detail1, detail3)
            else:
                if detail3 is None:
                    query_match = (f"SELECT {min_or_max}(match_date) FROM matches WHERE tournament_name=%s "
                                   "AND iteration=%s AND detail1=%s AND detail2=%s")
                    args_match = (tournament_name, iteration, detail1, detail2)
                else:
                    query_match = (f"SELECT {min_or_max}(match_date) FROM matches WHERE tournament_name=%s "
                                   "AND iteration=%s AND detail1=%s AND detail2=%s AND detail3=%s")
                    args_match = (tournament_name, iteration, detail1, detail2, detail3)
        cursor.execute(query_match, args_match)

        row = cursor.fetchone()
        while row is not None:
            result.append(row[0])
            row = cursor.fetchone()
        cursor.close()

        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        gen_conf = db_conf.read_general_config()
        if gen_conf["sql_output"] == "True":
            print(f"Reading {min_or_max}_DATE Match data of {tournament_name} iteration {iteration}"
                  f" detail1:{detail1}, detail2:{detail2}, detail3:{detail3} complete")
        return result


def read_match_all() -> list:
    """ Connect to MySQL database """

    db_config = db_conf.read_db_config()
    conn = None
    match_db = []

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            gen_conf = db_conf.read_general_config()
            if gen_conf["sql_output"] == "True":
                print('Importing match from MySQL database')

        cursor = conn.cursor()
        query_match = "SELECT * FROM matches;"
        args_match = tuple()
        cursor.execute(query_match, args_match)

        row = cursor.fetchone()
        while row is not None:
            current_match: match_data.Match = match_data.Match(
                row[1], row[2], row[3], row[4] == 1,
                row[5], row[6], row[7], row[8],
                row[9], row[10], row[11], row[12], row[13]
            )
            match_db.append(current_match)
            row = cursor.fetchone()
        cursor.close()

        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        match_db.sort(key=lambda x: x.match_date)
        gen_conf = db_conf.read_general_config()
        if gen_conf["sql_output"] == "True":
            print(f"Reading Match data complete")
        return match_db
