from metastruct import kishi_data, junni_info_generic
import re
import time
import urllib.request
import urllib.error


def import_junni() -> list:
    junni_list_list_dict = dict()
    try_count = 0
    while try_count < 50:
        try:
            print(f"Retrieving web information for tournament "
                  f"十段戦, please wait...")
            req = urllib.request.Request(
                f"http://47.56.124.126/shogititle.nobody.jp/ryuo_ft.html",
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
            html_str = str(html, encoding="Shift_JIS")
            shidan_start_index = html_str.find('<!-- 十段戦 -->')
            shidan_end_index = html_str.find('<!--about-->', shidan_start_index)
            shidan_content = html_str[shidan_start_index:shidan_end_index].split("\n")
            for shidan_content_row in shidan_content:
                re_complied = re.compile(
                    r'.*<a href="table/ryuo/judan-(\d+).*?'
                    r'<td.*?>(.*?)</td>.*?'
                    r'<td.*?>(.*?)</td>.*?'
                    r'(?P<result1><td.*?>)(?P<name1>.*?)</td>.*?'
                    r'(?P<result2><td.*?>)(?P<name2>.*?)</td>.*?'
                    r'(?P<result3><td.*?>)(?P<name3>.*?)</td>.*?'
                    r'(?P<result4><td.*?>)(?P<name4>.*?)</td>.*?'
                    r'(?P<result5><td.*?>)(?P<name5>.*?)</td>.*?'
                    r'(?P<result6><td.*?>)(?P<name6>.*?)</td>.*?'
                )
                re_result = re_complied.match(shidan_content_row)
                if re_result:
                    iteration = int(re_result.group(1))
                    junni_list_list = []
                    kishi1 = kishi_data.query_kishi_from_name(re_result.group("name1").replace("　", ""))
                    junni_list_list.append([kishi1, "1"])
                    kishi2 = kishi_data.query_kishi_from_name(re_result.group("name2").replace("　", ""))
                    junni_list_list.append([kishi2, "2"])
                    kishi3 = kishi_data.query_kishi_from_name(re_result.group("name3").replace("　", ""))
                    junni_list_list.append([kishi3, "3"])
                    kishi4 = kishi_data.query_kishi_from_name(re_result.group("name4").replace("　", ""))
                    junni_list_list.append([kishi4, "4"])
                    kishi5 = (kishi_data.query_kishi_from_name(re_result.group("name5").replace("　", ""))
                              if iteration != 11 else None)
                    if iteration == 11:
                        kishi5 = kishi_data.query_kishi_from_name("升田幸三")
                    junni_list_list.append([kishi5, "4" if iteration < 3 else "5"])
                    kishi6 = kishi_data.query_kishi_from_name(re_result.group("name6").replace("　", ""))
                    junni_list_list.append([kishi6, "4" if iteration < 3 else "5"])
                    if iteration == 11:
                        kishi7 = kishi_data.query_kishi_from_name("二上達也")
                        junni_list_list.append([kishi7, "5"])
                    results = []
                    for i in range(6):
                        results.append(re.match(r'.*?class="(.*?)".*?', re_result.group(f"result{i+1}")))
                    for i in range(6):
                        if results[i] is None:
                            junni_list_list[i].append("")
                        else:
                            junni_list_list[i].append(results[i].group(1))
                    if iteration == 11:
                        junni_list_list[6].append("down")
                    junni_list_list_dict[iteration] = junni_list_list
            result_list = []
            for k, v in junni_list_list_dict.items():
                for vv in v:
                    result_state = ""
                    if vv[2] == "down":
                        result_state = "downgrade"
                    elif vv[2] == "champ":
                        result_state = "challenge"
                    junni_info_item = junni_info_generic.JunniInfo("十段戦", k, vv[1], vv[0], result_state)
                    print(junni_info_item)
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
          f"for tournament 十段戦 "
          f"on large number of tries.")
    return []