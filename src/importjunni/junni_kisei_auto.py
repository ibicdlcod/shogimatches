from metastruct import kishi_data, junni_info_generic
import re
import time
import urllib.request
import urllib.error


def import_junni(iteration: int) -> list:
    if iteration < 66 or iteration > 71:
        return []
    try_count = 0
    while try_count < 50:
        try:
            print(f"Retrieving web information for tournament "
                  f"棋聖戦, please wait...")
            req = urllib.request.Request(
                f"http://47.56.124.126/shogititle.nobody.jp/table/kisei/kisei-{str(iteration).zfill(2)}.html",
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, '
                                  'like Gecko) Chrome/35.0.1916.47 Safari/537.36 '
                }
            )
            with urllib.request.urlopen(req) as response:
                html = response.read()
            html_str = str(html, encoding="Shift_JIS")
            kisei_start_index = html_str.find('棋聖戦三次予選')
            kisei_end_index = html_str.find('二次予選', kisei_start_index)
            kisei_content = html_str[kisei_start_index:kisei_end_index].split("\n")
            red_result_list = []
            white_result_list = []
            red_primitive_name_list = []
            white_primitive_name_list = []
            for kisei_content_row in kisei_content:
                re_complied = re.compile(
                    r'.*?│(?P<red_res>[○　])(?P<red>.*?)[＊△　]│.*'
                    r'　.*?│(?P<white_res>[○　])(?P<white>.*?)[＊△　]│.*'
                )
                re_complied2 = re.compile(
                    r'.*棋　士.*'
                )
                re_result = re_complied.match(kisei_content_row)
                re_result2 = re_complied2.match(kisei_content_row)
                if re_result and not re_result2:
                    red_result_list.append(re_result.group("red_res")[0])
                    white_result_list.append(re_result.group("white_res")[0])
                    red_primitive_name_list.append(re_result.group("red")[1:])
                    white_primitive_name_list.append(re_result.group("white")[1:])

            red_name_list = []
            for red_primitive_name in red_primitive_name_list:
                if red_primitive_name == "":
                    continue
                kishi_name_index = 0
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
                if white_primitive_name == "":
                    continue
                kishi_name_index = 0
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

                if i < 2:
                    junni_i = i + 1
                elif 2 <= i < 4:
                    junni_i = 3
                elif 4 <= i <= 6:
                    junni_i = i - 3
                else:
                    junni_i = 3

                result_i = "normal"
                if red_result_list[i] == "○":
                    result_i = "upgrade"
                junni_info_item = junni_info_generic.JunniInfo(
                    "棋聖戦",
                    iteration,
                    junni_i,
                    red_name_list[i],
                    result_i
                )
                result_list.append(junni_info_item)

            for i in range(len(white_name_list)):

                if i < 2:
                    junni_i = i + 1
                elif 2 <= i < 4:
                    junni_i = 3
                elif 4 <= i <= 6:
                    junni_i = i - 3
                else:
                    junni_i = 3

                result_i = "normal"

                if white_result_list[i] == "○":
                    result_i = "upgrade"
                junni_info_item = junni_info_generic.JunniInfo(
                    "棋聖戦",
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
          f"for tournament 棋聖戦 "
          f"on large number of tries.")
    return []
