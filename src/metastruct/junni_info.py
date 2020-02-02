from metastruct import kishi_data
import hashlib


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


# def junni_info_to_sql(in_info_list: list) -> None:
#     """ Connect to MySQL database """
#
#     db_config = db_conf.read_db_config()
#     conn = None
#
#     try:
#         conn = mysql.connector.MySQLConnection(**db_config)
#
#         if conn.is_connected():
#             gen_conf = db_conf.read_general_config()
#             if gen_conf["sql_output"] == "True":
#                 print('Exporting matches to MySQL database')
#
#         cursor = conn.cursor()
#         query_use = "USE shogi;"
#         args_use = tuple()
#         cursor.execute(query_use, args_use)
#
#         print('begin porting matches')
#
#         query_insert = ("INSERT INTO matches(hash,fiscal_year,"
#                         "match_date,win_loss_for_black,forfeit_active,"
#                         "black_name,white_name,iteration,tournament_name,"
#                         "detail1,detail2,detail3,mochishogi,sennichite)\n"
#                         "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,"
#                         "%s,%s,%s,%s,%s)\n"
#                         "ON DUPLICATE KEY UPDATE fiscal_year = VALUES(fiscal_year);")
#         for match in in_info_list:
#             args_insert = (match.hash, match.fiscal_year, match.match_date.isoformat(),
#                            match.win_loss_for_black, match.forfeit_active,
#                            match.black_name, match.white_name, match.iteration,
#                            match.tournament_name, match.detail1, match.detail2,
#                            match.detail3, match.mochishogi, match.sennichite)
#             cursor = conn.cursor()
#             cursor.execute(query_insert, args_insert)
#
#         if cursor.lastrowid:
#             print('last insert id', cursor.lastrowid)
#         else:
#             pass
#             # print('last insert id not found')  # Expected behaviour
#
#         cursor.close()
#         conn.commit()
#
#     except mysql.connector.Error as e:
#         print(e)
#
#     finally:
#         if conn is not None and conn.is_connected():
#             conn.close()