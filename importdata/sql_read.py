from metastruct import kishi_data, match_data
import metastruct.python_mysql_dbconf as db_conf
import mysql.connector


def read_kishi() -> list:
    """ Connect to MySQL database """

    db_config = db_conf.read_db_config()
    conn = None
    kishi_db = []

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connected to MySQL database')

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
        print("Reading Kishi data complete")
        return kishi_db


def read_match(tournament_name: str, iteration: str) -> list:
    """ Connect to MySQL database """

    db_config = db_conf.read_db_config()
    conn = None
    match_db = []

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connected to MySQL database')

        query_match = "SELECT * FROM matches WHERE tournament_name=%s AND iteration=%s"
        args_match = (tournament_name, iteration)
        cursor = conn.cursor()
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
        print("Reading Match data complete")
        return match_db
