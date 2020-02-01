from datetime import date
from metastruct import match_data
import importdata.python_mysql_dbconf as db_conf
import mysql.connector
import time
import urllib.request
import urllib.error


def import_junni(iteration: int) -> list:
    if iteration < 8 or iteration in list(range(31, 36)):
        print("Database have no such iteration for 順位戦")
        return []
    iteration_str = str(iteration).zfill(2)
    try_count = 0
    while try_count < 10:
        try:
            time.sleep(1)
            print(f"Retrieving web information for tournament "
                  f"順位戦 with iteration {iteration}, please wait...")
            req = urllib.request.Request(
                f"http://47.56.124.126/shogititle.nobody.jp/junisen/junisen-{iteration_str}.html",
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