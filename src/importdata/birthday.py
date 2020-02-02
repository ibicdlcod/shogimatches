from datetime import date
import time
import importdata.python_mysql_dbconf as db_conf
import mysql.connector
import urllib.request
import urllib.error


def gen_birthday(kishi_list: list):
    db_config_1 = db_conf.read_db_config('config\\db_config.ini', "kishi_query")
    delay = float(db_config_1["delay_birthday"])

    # birthday_dict = dict()
    for kishi in kishi_list:
        print(f"Obtaining birthday of {kishi.fullname}")
        birthday_from_sql = from_sql_birthday(kishi.id)
        if birthday_from_sql is not None:
            continue
        try_count = 0
        while try_count < 10:
            try:
                if delay > 0.0:
                    time.sleep(delay)
                with urllib.request.urlopen(f"http://kenyu1234.php.xdomain.jp/person.php?name={kishi.id}") as response:
                    html = response.read()
                html_str = str(html, encoding="utf-8-sig")
                index1 = html_str.find(f"生年月日")
                if index1 == -1:
                    to_sql_birthday(kishi.id, None)
                    break
                index2 = html_str.find("<td>", index1) + 4
                index3 = html_str.find("</td>", index2)
                to_sql_birthday(kishi.id, date.fromisoformat(html_str[index2:index3]))
                print(f"Obtained birthday of {kishi.fullname}")
                break
            except urllib.error.URLError as e:
                try_count += 1
                if hasattr(e, 'reason'):
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                elif hasattr(e, 'code'):
                    print('The server could not fulfill the request.')
                    print('Error code: ', e.code)
                time.sleep(1)
                continue
        else:
            print(f"Failed to obtain birthday of {kishi.fullname}"
                  f"on large number of tries.")


def to_sql_birthday(in_id: int, in_date) -> None:
    db_config = db_conf.read_db_config()
    conn = None

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        cursor = conn.cursor()
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        query_insert = ("INSERT INTO kishi(id, birthday)\n"
                        "VALUES(%s,%s)\n"
                        "ON DUPLICATE KEY UPDATE birthday = VALUES(birthday);")
        args_insert = (in_id, in_date.isoformat() if in_date is not None else None)
        cursor = conn.cursor()
        cursor.execute(query_insert, args_insert)

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def from_sql_birthday(in_id: int):
    db_config = db_conf.read_db_config()
    conn = None
    result = None

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        cursor = conn.cursor(buffered=True)
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        query_insert = ("SELECT id, birthday FROM kishi\n"
                        "WHERE id=%s;\n")
        args_insert = (in_id, )
        cursor = conn.cursor()
        cursor.execute(query_insert, args_insert)
        row = cursor.fetchall()
        if row is None:
            pass
        else:
            result = row[0][1]

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return result
