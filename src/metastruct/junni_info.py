from metastruct import kishi_data
import hashlib
import importdata.python_mysql_dbconf as db_conf
import mysql.connector


class JunniInfo:
    hash: bytearray
    iteration: int
    tier: str
    junni: int
    kishi: kishi_data.Kishi
    relegation_point_added: bool
    current_relegation_point: int
    result: str
    to_fc_year: int

    def __init__(self,
                 iteration,
                 tier,
                 junni,
                 kishi,
                 relegation_point_added,
                 current_relegation_point,
                 result,
                 to_fc_year):
        junni_code = (str(iteration) + tier
                      + str(junni).zfill(2) + kishi.fullname)
        h = hashlib.sha512()
        h.update(bytes(junni_code, "utf-8"))
        self.hash = h.digest()
        self.iteration = iteration
        self.tier = tier
        self.junni = junni
        self.kishi = kishi
        self.relegation_point_added = relegation_point_added
        self.current_relegation_point = current_relegation_point
        self.result = result
        self.to_fc_year = to_fc_year

    def __str__(self) -> str:
        out_str_item = [
                        # str(self.hash.hex()),
                        str(self.iteration),
                        self.tier,
                        str(self.junni),
                        self.kishi.fullname,
                        str(self.relegation_point_added),
                        str(self.current_relegation_point),
                        self.result,
                        str(self.to_fc_year)]
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

        query_insert = ("INSERT INTO junni(id_hash,iteration_int,"
                        "tier,junni,kishi_id,relegation_point_added,"
                        "current_relegation_point,result,to_fc_year)\n"
                        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)\n"
                        "ON DUPLICATE KEY UPDATE "
                        "iteration_int = VALUES(iteration_int), "
                        "tier = VALUES(tier), "
                        "junni = VALUES(junni), "
                        "kishi_id = VALUES(kishi_id), "
                        "relegation_point_added = VALUES(relegation_point_added), "
                        "current_relegation_point = VALUES(current_relegation_point), "
                        "result = VALUES(result), "
                        "to_fc_year = VALUES(to_fc_year)"
                        ";")
        for info in in_info_list:
            args_insert = (info.hash,
                           info.iteration,
                           info.tier,
                           info.junni,
                           info.kishi.id,
                           info.relegation_point_added,
                           info.current_relegation_point,
                           info.result,
                           info.to_fc_year)
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


def junni_info_from_sql(iteration_int: int):
    db_config = db_conf.read_db_config()
    conn = None
    result = []

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        cursor = conn.cursor(buffered=True)
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        query_insert = ("SELECT * FROM junni\n"
                        "WHERE iteration_int=%s;\n")
        args_insert = (iteration_int, )
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
                                              row[5] == 1,
                                              row[6],
                                              row[7],
                                              row[8])
                result.append(junni_info_result)

        cursor.close()
        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return result

