from datetime import date
import urllib.request


def import_data(self, iteration: int, tournament: int) -> str:
    with urllib.request.urlopen(f"http://kenyu1234.php.xdomain.jp/resultsm.php?sen=0"
                                f"&pd={1000+iteration}&mn={tournament}") as response:
        html = response.read()
    html_str = str(html, encoding="utf-8-sig")