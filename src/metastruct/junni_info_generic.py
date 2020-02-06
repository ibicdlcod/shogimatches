from metastruct import kishi_data
import hashlib
import importdata.python_mysql_dbconf as db_conf
import mysql.connector


class JunniInfo:
    hash: bytearray
    tournament_name: str
    iteration: int
    junni: int
    kishi: kishi_data.Kishi
    result: str

    def __init__(self,
                 tournament_name,
                 iteration,
                 junni,
                 kishi,
                 result,
                 ):
        junni_code = (str(iteration)
                      + str(junni).zfill(2)
                      + kishi.fullname)
        h = hashlib.sha512()
        h.update(bytes(junni_code, "utf-8"))
        self.hash = h.digest()

        self.tournament_name = tournament_name
        self.iteration = iteration
        self.junni = int(junni)
        self.kishi = kishi
        self.result = result

    def __str__(self) -> str:
        out_str_item = [
                        # str(self.hash.hex()),
                        self.tournament_name,
                        str(self.iteration),
                        str(self.junni),
                        self.kishi.fullname,
                        self.result,
        ]
        return ",".join(out_str_item)

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return self.hash == other.hash

    def __ne__(self, other):
        return self.hash != other.hash


def junni_info_to_sql(in_info_list: list) -> None:
    """ Connect to MySQL database """

    db_config = db_conf.read_db_config()
    conn = None

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            gen_conf = db_conf.read_general_config()
            if gen_conf["sql_output"] == "True":
                print('Exporting matches to MySQL database')

        cursor = conn.cursor()
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        print('begin porting junni')

        query_insert = ("INSERT INTO junni_other(id_hash,"
                        "tournament_name, iteration_int,"
                        "junni,kishi_id,result)\n"
                        "VALUES(%s,%s,%s,%s,%s,%s)\n"
                        "ON DUPLICATE KEY UPDATE "
                        "tournament_name = VALUES(tournament_name),"
                        "iteration_int = VALUES(iteration_int), "
                        "junni = VALUES(junni), "
                        "kishi_id = VALUES(kishi_id), "
                        "result = VALUES(result)"
                        ";")
        for info in in_info_list:
            args_insert = (info.hash,
                           info.tournament_name,
                           info.iteration,
                           info.junni,
                           info.kishi.id,
                           info.result,
                           )
            cursor = conn.cursor()
            cursor.execute(query_insert, args_insert)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            pass
            # print('last insert id not found')  # Expected behaviour

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def junni_info_from_sql(tournament_name: str, iteration_int: int):
    db_config = db_conf.read_db_config()
    conn = None
    result = []

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        cursor = conn.cursor(buffered=True)
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        query_insert = ("SELECT * FROM junni_other\n"
                        "WHERE tournament_name=%s AND iteration_int=%s;\n")
        args_insert = (tournament_name, iteration_int)
        cursor = conn.cursor()
        cursor.execute(query_insert, args_insert)
        rows = cursor.fetchall()
        if rows is None:
            return result
        else:
            for row in rows:
                junni_info_result = JunniInfo(row[1],
                                              row[2],
                                              row[3],
                                              kishi_data.query_kishi_from_id(row[4]),
                                              row[5],
                                              )
                result.append(junni_info_result)

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return result
