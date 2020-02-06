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
                  f"王位戦, please wait...")
            req = urllib.request.Request(
                f"http://47.56.124.126/shogititle.nobody.jp/table/oui/oui-{str(iteration).zfill(2)}.html",
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, '
                                  'like Gecko) Chrome/35.0.1916.47 Safari/537.36 '
                }
            )
            with urllib.request.urlopen(req) as response:
                html = response.read()
            html_str = str(html, encoding="Shift_JIS")
            oui_start_index = html_str.find('挑戦者決定リーグ')
            oui_end_index = html_str.find('予選', oui_start_index)
            oui_content = html_str[oui_start_index:oui_end_index].split("\n")
            red_result_list = []
            white_result_list = []
            red_primitive_name_list = []
            white_primitive_name_list = []
            for oui_content_row in oui_content:
                re_complied = re.compile(
                    r'.*?│(?P<red>.*?)│.*?勝.*?敗│.*?　.*?│(?P<white>.*?)│.*?勝.*?敗│'
                )
                re_result = re_complied.match(oui_content_row)
                if re_result:
                    red_result_list.append(re_result.group("red")[0])
                    white_result_list.append(re_result.group("white")[0])
                    red_primitive_name_list.append(re_result.group("red")[1:])
                    white_primitive_name_list.append(re_result.group("white")[1:])

            red_name_list = []
            for red_primitive_name in red_primitive_name_list:
                kishi_name_index = 1 if 27 < iteration < 56 else 0
                kishi_name = red_primitive_name[kishi_name_index]
                kishi = kishi_data.query_kishi_from_name(kishi_name)
                while kishi is None:
                    kishi_name_index += 1
                    if red_primitive_name[kishi_name_index] != '　':
                        kishi_name += red_primitive_name[kishi_name_index]
                    kishi = kishi_data.query_kishi_from_name(kishi_name)
                red_name_list.append(kishi)
            white_name_list = []
            for white_primitive_name in white_primitive_name_list:
                kishi_name_index = 1 if 27 < iteration < 56 else 0
                kishi_name = white_primitive_name[kishi_name_index]
                kishi = kishi_data.query_kishi_from_name(kishi_name)
                while kishi is None:
                    kishi_name_index += 1
                    if white_primitive_name[kishi_name_index] != '　':
                        kishi_name += white_primitive_name[kishi_name_index]
                    kishi = kishi_data.query_kishi_from_name(kishi_name)
                white_name_list.append(kishi)

            result_list = []
            
            for i in range(len(red_name_list)):

                junni_i = 0
                if iteration == 2:
                    junni_i = 1 if i < 1 else 2
                elif 2 < iteration < 27:
                    junni_i = 1 if i < 2 else 2
                elif 26 < iteration < 37:
                    junni_i = 1 if i < 2 else 2
                elif 36 < iteration:
                    junni_i = (i + 1) if i < 2 else 3

                result_i = "normal"
                if red_result_list[i] == "▼":
                    result_i = "downgrade"
                elif red_result_list[i] == "◎":
                    result_i = "challenge"
                elif red_result_list[i] == "○":
                    result_i = "playoff"
                junni_info_item = junni_info_generic.JunniInfo(
                    "王位戦",
                    iteration,
                    junni_i,
                    red_name_list[i],
                    result_i
                )
                result_list.append(junni_info_item)
                
            for i in range(len(white_name_list)):

                junni_i = 0
                if iteration == 2:
                    junni_i = 1 if i < 1 else 2
                elif 2 < iteration < 27:
                    junni_i = 1 if i < 2 else 2
                elif 26 < iteration < 37:
                    junni_i = 1 if i < 2 else 2
                elif 36 < iteration:
                    junni_i = (i + 1)

                result_i = "normal"
                if white_result_list[i] == "▼":
                    result_i = "downgrade"
                elif white_result_list[i] == "◎":
                    result_i = "challenge"
                elif white_result_list[i] == "○":
                    result_i = "playoff"
                junni_info_item = junni_info_generic.JunniInfo(
                    "王位戦",
                    iteration,
                    junni_i,
                    white_name_list[i],
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
          f"for tournament 王位戦 "
          f"on large number of tries.")
    return []
