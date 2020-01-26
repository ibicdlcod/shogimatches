from datetime import date
import urllib.request
import urllib.error
import time


def import_data(iteration: int, tournament: int) -> str:
    try_count = 0
    while try_count < 10:
        try:
            print("Retrieving web information, please wait...")
            with urllib.request.urlopen(f"http://kenyu1234.php.xdomain.jp/resultsm.php?sen=0"
                                        f"&pd={1000+iteration}&mn={tournament}") as response:
                html = response.read()
            html_str = str(html, encoding="utf-8-sig")
            # print(html_str)
            scroll_body_start = html_str.find("<tbody class=\"scrollBody\">")
            print(scroll_body_start)
            scroll_body_end = html_str.find("</tbody>\n</table>\n</div>")
            print(scroll_body_end)
            # return html_str
            return html_str[scroll_body_start+27:scroll_body_end]
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
    return ""
