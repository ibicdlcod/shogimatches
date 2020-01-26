from datetime import date
import urllib.request


def import_data(self, iteration: int) -> str:
    with urllib.request.urlopen(f"http://kenyu1234.php.xdomain.jp/resultsm.php?sen=0"
                                f"&pd={1000+iteration}&mn=1") as response:
        html = response.read()
    html_str = str(html, encoding="utf-8-sig")
    return html_str[index2 + 2 + len(self.fullname):index3]