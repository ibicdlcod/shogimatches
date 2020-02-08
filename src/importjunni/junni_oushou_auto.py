from metastruct import kishi_data, junni_info_generic
import re
import time
import urllib.request
import urllib.error


def import_junni(iteration: int) -> list:
    try_count = 0
    while try_count < 50:
        try:
            print(f"Retrieving web information for tournament "
                  f"王将戦, please wait...")
            req = urllib.request.Request(
                f"http://47.56.124.126/shogititle.nobody.jp/table/oushou/oushou-{str(iteration).zfill(2)}.html",
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, '
                                  'like Gecko) Chrome/35.0.1916.47 Safari/537.36 '
                }
            )
            with urllib.request.urlopen(req) as response:
                html = response.read()
            html_str = str(html, encoding="Shift_JIS")
            oushou_start_index = html_str.find('挑戦者決定リーグ')
            oushou_end_index = html_str.find('予選', oushou_start_index)
            oushou_content = html_str[oushou_start_index:oushou_end_index].split("\n")
            result_state_list = []
            primitive_name_list = []
            for oushou_content_row in oushou_content:
                re_complied = re.compile(
                    r'.*│(?P<g>.*?)│.*?勝.*?敗│.*?'
                )
                re_result = re_complied.match(oushou_content_row)
                if re_result:
                    result_state_list.append(re_result.group("g")[0])
                    primitive_name_list.append(re_result.group("g")[1:])

            name_list = []
            for primitive_name in primitive_name_list:
                kishi_name_index = 1 if iteration >= 43 else 0
                kishi_name = primitive_name[kishi_name_index]
                kishi = kishi_data.query_kishi_from_name(kishi_name)
                while kishi is None:
                    kishi_name_index += 1
                    if primitive_name[kishi_name_index] != '　':
                        kishi_name += primitive_name[kishi_name_index]
                    kishi = kishi_data.query_kishi_from_name(kishi_name)
                name_list.append(kishi)

            result_list = []

            for i in range(len(name_list)):
                if iteration >= 4:
                    junni_i = (i + 1) if i < 4 else 5
                elif iteration == 3:
                    junni_i = (i + 1) if i < 5 else 6
                elif iteration == 2:
                    junni_i = (i + 1) if i < 3 else 4
                else:
                    junni_i = 0

                result_i = "normal"
                if result_state_list[i] == "▼":
                    result_i = "downgrade"
                elif result_state_list[i] == "◎":
                    result_i = "challenge"
                elif result_state_list[i] == "○":
                    result_i = "playoff"
                junni_info_item = junni_info_generic.JunniInfo(
                    "王将戦",
                    iteration,
                    junni_i,
                    name_list[i],
                    result_i
                )
                result_list.append(junni_info_item)

            junni_info_generic.junni_info_to_sql(result_list)
            return result_list
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
    print(f"Failed to obtain junni information "
          f"for tournament 王将戦 "
          f"on large number of tries.")
    return []
