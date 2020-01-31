from datetime import date
from metastruct import kishi_rank_sql
from importdata import former_meijin
import mysql.connector
import importdata.python_mysql_dbconf as db_conf
import urllib.request
import urllib.error
import time


class Kishi:
    # defaults
    id: int = 0
    fullname: str = ""
    surname_length: int = 2
    wiki_name: str = ""  # Normally == fullname
    woman: bool = False
    current_shoreikai: bool = False
    current_amateur: bool = False

    # init begin
    def __init__(self,
                 init_id: int,
                 init_fullname: str,
                 init_sur_length: int,
                 init_wiki_name: str,
                 init_woman: bool,
                 init_cur_shoreikai: bool,
                 init_cur_amateur: bool,
                 ):
        self.id = init_id
        self.fullname = init_fullname
        self.surname_length = init_sur_length
        self.wiki_name = init_wiki_name
        self.woman = init_woman
        self.current_shoreikai = init_cur_shoreikai
        self.current_amateur = init_cur_amateur

    def __hash__(self):
        return self.id

    def __str__(self) -> str:
        out_str_item = [str(self.id),
                        self.fullname,
                        str(self.surname_length),
                        self.wiki_name,
                        "T" if self.woman else "F",
                        "T" if self.current_shoreikai else "F",
                        "T" if self.current_amateur else "F",
                        ]
        return ",".join(out_str_item)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def rank(self, query_date: date) -> tuple:
        sql_result = kishi_rank_sql.from_sql(self.id, query_date)
        if (sql_result is not None) and sql_result.endswith("段"):
            former_ryuou_name = former_meijin.import_former_ryuou(query_date)
            if former_ryuou_name == self.fullname:
                sql_result = "前竜王"
            former_meijin_name = former_meijin.import_former_meijin(query_date)
            if former_meijin_name == self.fullname:
                sql_result = "前名人"
        if sql_result is not None:
            if len(sql_result) > 3:
                length = len(sql_result) * 0.7
                sql_result = "<small>" + sql_result + "</small>"
            else:
                length = len(sql_result)
            return sql_result, length

        try_count = 0
        while try_count < 10:
            try:
                time.sleep(0.2)
                print(f"Obtaining rank of {self.fullname} "
                      f"on day {query_date.isoformat()} ")
                with urllib.request.urlopen(f"http://kenyu1234.php.xdomain.jp/titlecheck.php?name={self.id}"
                                            f"&date={date.isoformat(query_date)}") as response:
                    html = response.read()
                html_str = str(html, encoding="utf-8-sig")
                index1 = html_str.find(f"person.php?name={self.id}\"")
                index2 = html_str.find(">", index1+8)
                index3 = [i for i in range(index2, index2+100)
                          if html_str[i] == "<"
                          or html_str[i] == "("
                          or html_str[i] == "・"][0]
                if html_str[index3] == "・" and html_str[index3-2] == "竜" and html_str[index3-3] == " ":
                    result = "竜王名人"
                else:
                    result = html_str[index2 + 2 + len(self.fullname):index3]
                if (result is not None) and result.endswith("段"):
                    former_ryuou_name = former_meijin.import_former_ryuou(query_date)
                    if former_ryuou_name == self.fullname:
                        result = "前竜王"
                    former_meijin_name = former_meijin.import_former_meijin(query_date)
                    if former_meijin_name == self.fullname:
                        result = "前名人"
                kishi_rank_sql.to_sql(result, self.id, query_date)
                print(f"Obtained rank of {self.fullname} "
                      f"on day {query_date.isoformat()} ")
                if len(result) > 3:
                    length = len(result) * 0.7
                    result = "<small>" + result + "</small>"
                else:
                    length = len(result)
                return result, length
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
        # try failed
        print(f"Failed to obtain rank of {self.fullname}"
              f"on day {query_date.isoformat()} "
              f"on large number of tries.")
        return "", 0


def kishi_from_str(in_str: str):
    a = in_str.split(",")
    return Kishi(int(a[0]), a[1], int(a[2]), a[3],
                 True if a[4] == 'T' else False,
                 True if a[5] == 'T' else False,
                 True if a[6] == 'T' else False,
                 )


def query_kishi_from_name(in_name: str) -> Kishi:
    db_config = db_conf.read_db_config()
    conn = None
    result = None

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        cursor = conn.cursor(buffered=True)
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        query_insert = ("SELECT * FROM kishi\n"
                        "WHERE fullname=%s;\n")
        args_insert = (in_name,)
        cursor = conn.cursor()
        cursor.execute(query_insert, args_insert)
        all_rows = cursor.fetchall()
        row = all_rows[0]
        if row is None:
            print(f"Invalid name: kishi {in_name} does not exist")
            result = None
        else:
            result = Kishi(row[0], row[1], row[2], row[3], row[4] == 1,
                           row[5] == 1, row[6] == 1)

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return result


def query_kishi_from_id(in_id: int) -> Kishi:
    db_config = db_conf.read_db_config()
    conn = None
    result = None

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        cursor = conn.cursor(buffered=True)
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        query_insert = ("SELECT * FROM kishi\n"
                        "WHERE id=%s;\n")
        args_insert = (in_id,)
        cursor = conn.cursor()
        cursor.execute(query_insert, args_insert)
        all_rows = cursor.fetchall()
        row = all_rows[0]
        if row is None:
            print(f"Invalid name: kishi {in_id} does not exist")
            result = None
        else:
            result = Kishi(row[0], row[1], row[2], row[3], row[4] == 1,
                           row[5] == 1, row[6] == 1)

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return result
