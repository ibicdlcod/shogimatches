import hashlib
from datetime import date
import mysql.connector
import metastruct.python_mysql_dbconf as db_conf


def to_sql(in_str: str, in_id: int, in_date: date) -> None:
    db_config = db_conf.read_db_config()
    conn = None

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        cursor = conn.cursor()
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        rank_code = (in_date.isoformat()
                     + " " + str(in_id))
        h = hashlib.sha512()
        h.update(bytes(rank_code, "utf-8"))
        rank_hash = h.digest()

        query_insert = ("INSERT INTO ranking(id_hash, id, on_date, rank_text)\n"
                        "VALUES(%s,%s,%s,%s)\n"
                        "ON DUPLICATE KEY UPDATE rank_text = VALUES(rank_text);")
        args_insert = (rank_hash, in_id, in_date.isoformat(), in_str)
        cursor = conn.cursor()
        cursor.execute(query_insert, args_insert)

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def from_sql(in_id: int, in_date: date):
    db_config = db_conf.read_db_config()
    conn = None
    result = None

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        cursor = conn.cursor(buffered=True)
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        query_insert = ("SELECT rank_text FROM ranking\n"
                        "WHERE id=%s AND on_date=%s;\n")
        args_insert = (in_id, in_date.isoformat())
        cursor = conn.cursor()
        cursor.execute(query_insert, args_insert)
        row = cursor.fetchall()
        if row is None:
            pass
        else:
            result = row[0][0]

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return result
