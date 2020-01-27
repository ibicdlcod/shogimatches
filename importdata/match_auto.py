from datetime import date
from metastruct import match_data
import metastruct.python_mysql_dbconf as db_conf
import mysql.connector
import urllib.request
import urllib.error
import time


def str_to_match(in_str: str) -> match_data.Match:
    in_str_frag = in_str.split("</td>\n")

    proto_fiscal = in_str_frag[0]
    fiscal_index = proto_fiscal.find(";\">") + 3
    fiscal = int(proto_fiscal[fiscal_index:])

    proto_date = in_str_frag[1]
    date_index = proto_date.find(";\">") + 3
    date_eff = date.fromisoformat(proto_date[date_index:])

    proto_result = in_str_frag[2]
    if len(proto_result) == 4:
        result = ''  # 1956-01-26 高島一岐代 vs 灘蓮照 無勝負
    else:
        result = proto_result[4]
    black_win = 0
    forfeit = False
    if result == '○':
        black_win = 1
    elif result == '□':
        black_win = 1
        forfeit = True
    elif result == '●':
        black_win = -1
    elif result == '■':
        black_win = -1
        forfeit = True
    elif result == '持' or result == '':
        black_win = 0

    black_name = in_str_frag[3][4:]
    white_name = in_str_frag[4][4:]
    iteration = in_str_frag[6][4:]
    tournament_name = in_str_frag[7][4:]
    detail1 = in_str_frag[8][4:]

    proto_detail2 = in_str_frag[9]
    detail2_index = proto_detail2.find(";\">") + 3
    detail2 = proto_detail2[detail2_index:]
    proto_detail3 = in_str_frag[10]
    detail3_index = proto_detail3.find(";\">") + 3
    detail3 = proto_detail3[detail3_index:]

    proto_mochishogi = in_str_frag[11]
    mochishogi_index = proto_mochishogi.find(";\">") + 3
    mochishogi = int("0" + proto_mochishogi[mochishogi_index:])
    proto_sennichite = in_str_frag[12]
    sennichite_index = proto_sennichite.find(";\">") + 3
    sennichite = int("0" + proto_sennichite[sennichite_index:])

    return_value = match_data.Match(fiscal, date_eff, black_win, forfeit, black_name, white_name,
                                    iteration, tournament_name, detail1, detail2, detail3,
                                    mochishogi, sennichite)
    return return_value


def import_data(iteration: int, tournament: int) -> list:
    try_count = 0
    while try_count < 10:
        try:
            time.sleep(1)
            print(f"Retrieving web information for tournament "
                  f"{tournament} with iteration {iteration}, please wait...")
            req = urllib.request.Request(
                f"http://kenyu1234.php.xdomain.jp/resultsm.php?sen=0"
                f"&pd={1000 + iteration}&mn={tournament}",
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, '
                                  'like Gecko) Chrome/35.0.1916.47 Safari/537.36 '
                }
            )
            with urllib.request.urlopen(req) as response:
                # with urllib.request.urlopen(f"http://kenyu1234.php.xdomain.jp/resultsm.php?sen=0"
                #                             f"&pd={1000 + iteration}&mn={tournament}") as response:
                html = response.read()
            html_str = str(html, encoding="utf-8-sig")
            scroll_body_start = html_str.find("<tbody class=\"scrollBody\">") + 27
            scroll_body_end = html_str.find("</tbody>\n</table>\n</div>")
            real_content = html_str[scroll_body_start:scroll_body_end]
            real_contents = real_content.split("</tr>")
            real_contents.pop(-1)
            # return html_str
            return_value = []
            for item in real_contents:
                return_value.append(str_to_match(item))
            return return_value
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
    print(f"Failed to obtain iteration of {iteration}"
          f"for tournament {tournament} "
          f"on large number of tries.")
    return []


def match_to_sql(in_match_list: list) -> None:
    """ Connect to MySQL database """

    db_config = db_conf.read_db_config()
    conn = None

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connected to MySQL database')

        cursor = conn.cursor()
        query_use = "USE shogi;"
        args_use = tuple()
        cursor.execute(query_use, args_use)

        print('begin porting matches')

        query_insert = ("INSERT INTO matches(hash,fiscal_year,"
                        "match_date,win_loss_for_black,forfeit_active,"
                        "black_name,white_name,iteration,tournament_name,"
                        "detail1,detail2,detail3,mochishogi,sennichite)\n"
                        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                        "%s,%s,%s,%s,%s)\n"
                        "ON DUPLICATE KEY UPDATE fiscal_year = VALUES(fiscal_year);")
        for match in in_match_list:
            args_insert = (match.hash, match.fiscal_year, match.match_date.isoformat(),
                           match.win_loss_for_black, match.forfeit_active,
                           match.black_name, match.white_name, match.iteration,
                           match.tournament_name, match.detail1, match.detail2,
                           match.detail3, match.mochishogi, match.sennichite)
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
