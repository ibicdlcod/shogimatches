import importdata
from metastruct import kisei_data
import metastruct.python_mysql_dbconf as db_conf
import mysql.connector


def read_kisei() -> list:
    """ Connect to MySQL database """

    db_config = db_conf.read_db_config()
    conn = None
    kisei_db = []

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connected to MySQL database')

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM kisei")

        row = cursor.fetchone()
        while row is not None:
            current_kisei: kisei_data.Kisei = kisei_data.Kisei(
                row[0], row[1], row[2], row[3], row[4] == 1,
                row[5] == 1, row[6] == 1
            )
            kisei_db.append(current_kisei)
            row = cursor.fetchone()
        cursor.close()

        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        kisei_db.sort(key=lambda x: x.id)
        return kisei_db