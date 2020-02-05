from datetime import date
from importdata import birthday, former_meijin
from metastruct import kishi_rank_sql
import mysql.connector
import importdata.python_mysql_dbconf as db_conf
import time
import urllib.request
import urllib.error


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
        db_config_1 = db_conf.read_db_config('config\\db_config.ini', "kishi_query")
        delay = float(db_config_1["delay_rank"])

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
        while try_count < 50:
            try:
                if delay > 0.0:
                    time.sleep(delay)
                print(f"Obtaining rank of {self.fullname} "
                      f"on day {query_date.isoformat()} ")
                with urllib.request.urlopen(f"http://kenyu1234.php.xdomain.jp/titlecheck.php?name={self.id}"
                                            f"&date={date.isoformat(query_date)}") as response:
                    html = response.read()
                html_str = str(html, encoding="utf-8-sig")
                index1 = html_str.find(f"person.php?name={self.id}\"")
                index2 = html_str.find(">", index1 + 8)
                index3 = [i for i in range(index2, index2 + 100)
                          if html_str[i] == "<"
                          or html_str[i] == "("
                          or html_str[i] == "・"][0]
                if html_str[index3] == "・" and html_str[index3 - 2] == "竜" and html_str[index3 - 3] == " ":
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

    def birthday(self):
        db_config_1 = db_conf.read_db_config('config\\db_config.ini', "kishi_query")
        delay = float(db_config_1["delay_birthday"])
        if delay > 0.0:
            time.sleep(delay)
        return birthday.from_sql_birthday(self.id)

    def get_full_wiki_name(self):
        display_length = len(self.fullname)
        if self.wiki_name == "":
            kishi_display_name = ("[["
                                  + self.fullname
                                  + "]]")
        else:
            kishi_display_name = ("[["
                                  + self.wiki_name
                                  + "|"
                                  + self.fullname
                                  + "]]")
        return kishi_display_name, display_length


def kishi_from_str(in_str: str):
    a = in_str.split(",")
    return Kishi(int(a[0]), a[1], int(a[2]), a[3],
                 True if a[4] == 'T' else False,
                 True if a[5] == 'T' else False,
                 True if a[6] == 'T' else False,
                 )


kishi_name_to_kishi_dict = dict()


def query_kishi_from_name(in_name_pri: str) -> Kishi:
    if in_name_pri in kishi_name_to_kishi_dict.keys():
        return kishi_name_to_kishi_dict[in_name_pri]

    db_config_2 = db_conf.read_db_config('config\\db_config.ini', "sql_general")
    if db_config_2["sql_output"] == "True":
        print(f"Query Kishi data for {in_name_pri}, please wait...")

    db_config_1 = db_conf.read_db_config('config\\db_config.ini', "kishi_query")
    delay = float(db_config_1["delay_name"])

    if delay > 0.0:
        time.sleep(delay)
    if in_name_pri == "高野秀行":
        in_name = "髙野秀行"
    elif in_name_pri == "高崎一生":
        in_name = "髙﨑一生"
    elif in_name_pri == "高見泰地":
        in_name = "髙見泰地"
    elif in_name_pri == "高野智史":
        in_name = "髙野智史"
    elif in_name_pri == "平藤真吾":
        in_name = "平藤眞吾"
    elif in_name_pri == "広津久雄":
        in_name = "廣津久雄"
    elif in_name_pri == "松田茂行":
        in_name = "松田茂役"
    elif in_name_pri == "森&#38622;二":
        in_name = "森雞二"
    elif in_name_pri == "田中正之":
        in_name = "田中魁秀"
    elif in_name_pri == "吉田正和":
        in_name = "渡辺正和"
    else:
        in_name = in_name_pri

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
        if len(all_rows) == 0:
            if db_config_2["sql_output"] == "True":
                print(f"Invalid name: kishi {in_name} does not exist")
            result = None
            kishi_name_to_kishi_dict[in_name_pri] = result
        row = all_rows[0]
        if row is None:
            if db_config_2["sql_output"] == "True":
                print(f"Invalid name: kishi {in_name} does not exist")
            result = None
            kishi_name_to_kishi_dict[in_name_pri] = result
        else:
            result = Kishi(row[0], row[1], row[2], row[3], row[4] == 1,
                           row[5] == 1, row[6] == 1)
            kishi_name_to_kishi_dict[in_name_pri] = result

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return result


def query_kishi_from_id(in_id: int):
    db_config = db_conf.read_db_config()
    conn = None

    try_count = 0
    while try_count < 50:
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
            else:
                result = Kishi(row[0], row[1], row[2], row[3], row[4] == 1,
                               row[5] == 1, row[6] == 1)
                cursor.close()
                conn.commit()
                return result

            cursor.close()
            conn.commit()

        except mysql.connector.Error as e:
            print(e)
            time.sleep(1)
            try_count += 1
            continue

        finally:
            if conn is not None and conn.is_connected():
                conn.close()
    print(f"Failed to obtain kishi data of {in_id} "
          f"on large number of tries.")
    return None


dict_rank_to_int = {
    "<small>竜王名人</small>": 100,
    "竜王": 99,
    "名人": 98,
    "五冠": 95,
    "四冠": 94,
    "三冠": 93,
    "二冠": 92,
    "十段": 89,
    "叡王": 88,
    "王位": 87,
    "王座": 86,
    "棋王": 85,
    "王将": 84,
    "棋聖": 83,
    "前名人": 82,
    "前竜王": 81,
    "<small>十四世名人</small>": 79,
    "<small>十五世名人</small>": 78,
    "<small>十六世名人</small>": 77,
    "<small>永世十段</small>": 71,
    "<small>名誉十段</small>": 70,
    "<small>実力制第四代名人</small>": 67,
    "<small>永世王位</small>": 66,
    "<small>名誉王座</small>": 65,
    "<small>永世棋王</small>": 64,
    "<small>永世王将</small>": 63,
    "<small>永世棋聖</small>": 62,
    "<small>名誉名人</small>": 61,
    "九段": 60,
    "<small>名誉九段</small>": 59,
    "八段": 58,
    "七段": 57,
    "六段": 56,
    "五段": 55,
    "四段": 54,
    "<small>女流六冠</small>": 46,
    "<small>女流五冠</small>": 45,
    "<small>女流四冠</small>": 44,
    "<small>女流三冠</small>": 43,
    "<small>女流二冠</small>": 42,
    "清麗": 39,
    "女王": 38,
    "<small>女流王座</small>": 37,
    "<small>女流名人</small>": 36,
    "<small>女流王位</small>": 35,
    "<small>女流王将</small>": 34,
    "<small>倉敷藤花</small>": 33,
    "<small>女流六段</small>": 27,
    "<small>女流五段</small>": 26,
    "<small>女流四段</small>": 25,
    "三段": 24,
    "<small>女流三段</small>": 23,
    "<small>女流二段</small>": 22,
    "<small>女流初段</small>": 21,
    "<small>女流1級</small>": 19,
    "<small>女流2級</small>": 18,
    "<small>女流3級</small>": 17,
    "アマ": 1,
    "": 0,
}


def rank_to_int(in_str):
    return dict_rank_to_int[in_str]
