from metastruct import kishi_data
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


def read_match(tournament_id: int, iteration_id: int) -> list:
    pass
