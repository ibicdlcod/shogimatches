from datetime import date
import urllib.request
import urllib.error
import time


def kisei_from_str(in_str: str):
    a = in_str.split(",")
    return Kisei(int(a[0]), a[1], int(a[2]), a[3],
                 True if a[4] == 'T' else False,
                 True if a[5] == 'T' else False,
                 True if a[6] == 'T' else False,
                 )


class Kisei:
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

    # init end

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

    def rank(self, query_date: date) -> str:
        try_count = 0
        while try_count < 10:
            try:
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
                    return "竜王名人"
                else:
                    return html_str[index2 + 2 + len(self.fullname):index3]
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
        return ""
