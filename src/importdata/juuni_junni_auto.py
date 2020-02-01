from metastruct import kishi_data, junni_info
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
            html_str = str(html, encoding="Shift_JIS")
            process_junni_html_all(html_str, iteration)
            return []
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
          f"for tournament 順位戦 "
          f"on large number of tries.")
    return []


def process_junni_html_all(in_str, iteration):
    result_list = []
    meijin_scroll_body_start = in_str.find('class="champ">')
    meijin_scroll_body_end = in_str.find('</td>', meijin_scroll_body_start)
    content = in_str[meijin_scroll_body_start:meijin_scroll_body_end]
    result_list += process_junni_html_meijin(content, iteration)

    a_scroll_body_start = in_str.find("<!--Ａ級-->")
    a_scroll_body_end = in_str.find("<!--スペース-->", a_scroll_body_start)
    content = in_str[a_scroll_body_start:a_scroll_body_end]
    result_list += process_junni_html(content, iteration, "A")
    b1_scroll_body_start = in_str.find("<!--Ｂ級１組-->")
    b1_scroll_body_end = in_str.find("<!--スペース-->", b1_scroll_body_start)
    content = in_str[b1_scroll_body_start:b1_scroll_body_end]
    result_list += process_junni_html(content, iteration, "B1")
    b2_scroll_body_start = in_str.find("<!--Ｂ級２組-->")
    b2_scroll_body_end = in_str.find("<!--スペース-->", b2_scroll_body_start)
    content = in_str[b2_scroll_body_start:b2_scroll_body_end]
    result_list += process_junni_html(content, iteration, "B2")
    c1_scroll_body_start = in_str.find("<!--Ｃ級１組-->")
    c1_scroll_body_end = in_str.find("<!--スペース-->", c1_scroll_body_start)
    content = in_str[c1_scroll_body_start:c1_scroll_body_end]
    result_list += process_junni_html(content, iteration, "C1")
    c2_scroll_body_start = in_str.find("<!--Ｃ級２組-->")
    c2_scroll_body_end = in_str.find("<!--スペース-->", c2_scroll_body_start)
    content = in_str[c2_scroll_body_start:c2_scroll_body_end]
    result_list += process_junni_html(content, iteration, "C2")

    if iteration >= 53:
        fc_scroll_body_start = in_str.find("<!--フリークラス-->")
        fc_scroll_body_end = in_str.find("<!--貼り付けここまで-->", fc_scroll_body_start)
        content = in_str[fc_scroll_body_start:fc_scroll_body_end]
        result_list += process_junni_html_fc(content, iteration)
    print(result_list)


def process_junni_html(in_str, iteration, tier):
    # a_scroll_body_start = in_str.find("<!--Ａ級-->")
    # a_scroll_body_end = in_str.find("<!--スペース-->", a_scroll_body_start)
    # content = in_str[a_scroll_body_start:a_scroll_body_end]
    contents = in_str.split("</tr>")
    real_contents = []
    result_list = []
    for row in contents:
        if row.find("</td><td") != -1:
            real_contents.append(row)
    # 棋士名：寻找title="再找">
    for i in range(len(real_contents)):
        result = "normal"

        real_row = real_contents[i]

        kishi_name_index = real_row.find('title="')
        kishi_name_index = real_row.find('">', kishi_name_index) + 2
        if kishi_name_index == 1:
            real_kishi = None
        else:
            kishi_name = real_row[kishi_name_index]
            while kishi_data.query_kishi_from_name(kishi_name) is None:
                kishi_name_index += 1
                if real_row[kishi_name_index] != '　':
                    kishi_name += real_row[kishi_name_index]
            real_kishi_name = kishi_name
            real_kishi = kishi_data.query_kishi_from_name(real_kishi_name)

        relegation_point_added = False
        if real_row.find("▼") != -1:
            relegation_point_added = True
        allowed_relegation_point = 2
        if real_row.find("kokyu") != -1:
            if real_row.find("kokyu1") != -1:
                allowed_relegation_point = 1
            elif real_row.find("kokyu0") != -1:
                allowed_relegation_point = 0
        current_relegation_point = 0
        if tier == "A" or tier == "B1":
            current_relegation_point = 0
        elif tier == "B2" or tier == "C1":
            current_relegation_point = 0 if allowed_relegation_point == 2 else 1
        elif tier == "C2":
            current_relegation_point = 2 - allowed_relegation_point

        if real_row.find('class="champ"') != -1:
            result = "challenge"
        elif real_row.find('class="challenge"') != -1:
            result = "playoff"
        elif real_row.find('class="up"') != -1:
            result = "upgrade"
        elif real_row.find('class="down"') != -1:
            result = "downgrade"
        elif real_row.find('class="fc"') != -1:
            result = "to_fc"
        elif real_row.find('class="revive"') != -1:
            result = "minus_point"
        elif real_row.find('class="absent"') != -1:
            result = "absent"
        elif real_row.find('class="retire"') != -1:
            result = "retire"
        elif real_row.find('class="dead"') != -1:
            result = "dead"

        if real_kishi is not None:
            print(iteration,
                  tier,
                  i + 1,
                  real_kishi.fullname,
                  relegation_point_added,
                  current_relegation_point,
                  result,
                  None)
            result_list.append(junni_info.JunniInfo(
                iteration,
                tier,
                i + 1,
                real_kishi,
                relegation_point_added,
                current_relegation_point,
                result,
                None
            ))
        else:
            pass
    return result_list


def process_junni_html_fc(in_str, iteration):
    contents = in_str.split("</tr>")
    real_contents1 = []
    real_contents2 = []
    part_1_flag = False
    part_2_flag = False
    result_list = []

    for row in contents:
        if row.find("転出年度") != -1:
            part_1_flag = True
        elif row.find("編入年度") != -1:
            part_1_flag = False
            part_2_flag = True
        elif row.find("</td><td") != -1:
            if part_1_flag:
                real_contents1.append(row)
            elif part_2_flag:
                real_contents2.append(row)
    for i in range(len(real_contents1)):
        real_row = real_contents1[i]

        if real_row.find('">') != -1:
            kishi_name_index = real_row.find('">') + 2
        elif real_row.find('<tr><td>') == -1:
            continue
        else:
            kishi_name_index = real_row.find('<tr><td>') + 8
        kishi_name = real_row[kishi_name_index]
        while kishi_data.query_kishi_from_name(kishi_name) is None:
            kishi_name_index += 1
            if real_row[kishi_name_index] != '　':
                kishi_name += real_row[kishi_name_index]
        real_kishi_name = kishi_name
        real_kishi = kishi_data.query_kishi_from_name(real_kishi_name)
        kishi_year_index = real_row.find('</td><td>', kishi_name_index) + 9

        print(iteration,
              "FC",
              0,
              real_kishi.fullname,
              False,
              0,
              "f_announce",
              int(real_row[kishi_year_index:kishi_year_index + 4])
              )
        result_list.append(junni_info.JunniInfo(
            iteration,
            "FC",
            0,
            real_kishi,
            False,
            0,
            "f_announce",
            int(real_row[kishi_year_index:kishi_year_index + 4])
        ))

    for i in range(len(real_contents2)):
        real_row = real_contents2[i]

        if real_row.find('">') != -1:
            kishi_name_index = real_row.find('">') + 2
        elif real_row.find('<tr><td>') == -1:
            continue
        else:
            kishi_name_index = real_row.find('<tr><td>') + 8
        kishi_name = real_row[kishi_name_index]
        while kishi_data.query_kishi_from_name(kishi_name) is None:
            kishi_name_index += 1
            if real_row[kishi_name_index] != '　':
                kishi_name += real_row[kishi_name_index]
        real_kishi_name = kishi_name
        real_kishi = kishi_data.query_kishi_from_name(real_kishi_name)
        kishi_year_index = real_row.find('</td><td>', kishi_name_index) + 9

        print(iteration,
              "FC",
              0,
              real_kishi.fullname,
              False,
              0,
              "f_relegated",
              int(real_row[kishi_year_index:kishi_year_index + 4])
              )
        result_list.append(junni_info.JunniInfo(
            iteration,
            "FC",
            0,
            real_kishi,
            False,
            0,
            "f_relegated",
            int(real_row[kishi_year_index:kishi_year_index + 4])
        ))
    return result_list


def process_junni_html_meijin(in_str, iteration):
    real_row = in_str[14:]
    result_list = []

    kishi_name_index = 0
    kishi_name = real_row[kishi_name_index]
    while kishi_data.query_kishi_from_name(kishi_name) is None:
        kishi_name_index += 1
        if real_row[kishi_name_index] != '　':
            kishi_name += real_row[kishi_name_index]
    real_kishi_name = kishi_name
    real_kishi = kishi_data.query_kishi_from_name(real_kishi_name)
    print(iteration + 1,
          "M",
          0,
          real_kishi.fullname,
          False,
          0,
          "normal",
          None
          )
    result_list.append(junni_info.JunniInfo(
        iteration + 1,
        "M",
        0,
        real_kishi,
        False,
        0,
        "normal",
        None
    ))
    return result_list
