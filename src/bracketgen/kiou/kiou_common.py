from bracketgen import title_match, lea_from_mat
from importdata import sql_read
from metastruct import organized_tr, kishi_data


def kiou_title_matches(iteration_int: int):
    iteration_str = f"第{str(iteration_int).zfill(2)}期"
    iteration_str_prev = (f"第{str(iteration_int - 1).zfill(2)}期"
                          if iteration_int != 1
                          else "第1回")
    # 五番勝負
    title_length_str = "五番勝負" if iteration_int != 1 else ""
    title_length_str_prev = "五番勝負" if iteration_int > 2 else ""
    title_matches = sql_read.read_match("棋王戦", iteration_str, "タイトル戦", title_length_str)
    org_tree_title = organized_tr.OrganizedTree(title_matches, f"タイトル戦" + title_length_str, ["", ])
    if iteration_int > 2:
        title_matches_last = sql_read.read_match("棋王戦", iteration_str_prev, "タイトル戦", title_length_str_prev)
        org_tree_title_last = organized_tr.OrganizedTree(title_matches_last, f"タイトル戦" + title_length_str_prev,
                                                         ["", ])
        return title_match.title_match_str_plus(org_tree_title,
                                                "棋王戦",
                                                iteration_str,
                                                "棋王",
                                                title_length_str,
                                                org_tree_title_last)
    elif iteration_int == 2:
        return title_match.title_match_str_plus2(org_tree_title,
                                                 "棋王戦",
                                                 iteration_str,
                                                 "棋王",
                                                 title_length_str,
                                                 kishi_data.query_kishi_from_name("大内延介"))
    else:
        return None


def kiou_title_group(iteration_int: int):
    result_list_list = []

    iteration_str = f"第{str(iteration_int).zfill(2)}期"
    junni_matches = sql_read.read_match("棋王戦", iteration_str, "決勝リーグ戦", "")
    league_info_db = lea_from_mat.gen_lea_pos_no_round_names(junni_matches)

    participants = []
    for league_info in league_info_db:
        participants.append(league_info.kishi)
        this_id = league_info.kishi.id
        this_kishi = league_info.kishi
        last_match_date = league_info.last_match_date
        this_rank = this_kishi.rank(last_match_date)
        display_length = len(this_kishi.fullname)
        kishi_display_name = this_kishi.get_full_wiki_name()[0]
        junni = ""
        if this_kishi.fullname == "内藤國雄":
            junni = "前回棋王"
        elif this_kishi.fullname == "高島弘光":
            junni = "全勝通過"
        elif this_kishi.fullname == "大内延介":
            junni = "敗者復活"
        result_list_list.append([
            iteration_int,
            junni,
            kishi_display_name + this_rank[0],
            display_length + this_rank[1],
            league_info.wins,
            league_info.losses,
            "normal" if this_kishi == kishi_data.query_kishi_from_name("高島弘光") else "playoff",
            league_info,
            this_id,
        ])
    result = draw_table_kiou_group(result_list_list)

    return result


def draw_table_kiou_group(in_list_list: list):
    result = ""
    max_name_length = 0
    round_length = 0
    relegated_num = 0
    content_length = dict()

    for in_list in in_list_list:
        max_name_length = max(max_name_length, in_list[3])
        current_info_round_num = in_list[7].round_num if in_list[7] is not None else 0
        round_length = max(round_length, current_info_round_num)

        for round_j in range(current_info_round_num):
            if round_j not in content_length.keys():
                content_length[round_j] = in_list[7].output_detail_lengths[round_j]
            else:
                content_length[round_j] = max(content_length[round_j],
                                              in_list[7].output_detail_lengths[round_j])
        if in_list[6] == "downgrade":
            relegated_num += 1

    result += f""

    content_size = 0
    for round_i in range(round_length):
        content_size += (content_length[round_i])
    content_size += max_name_length + 1
    font_size = 1400 / (content_size / 3 + 9)
    font_size_eff = max(50.0, font_size)
    result += ('{|class="wikitable plainrowheaders sortable" style="text-align:center; font-size: %f%%;"\n'
               % (font_size,))
    result += '|-\n'
    result += (f'!順位!!style="width:{max_name_length * 0.03 * font_size_eff}em" class="unsortable"|棋士'
               f'!!勝!!負!!class="unsortable"|備考')
    for round_i in range(round_length):
        result += f'!!style="width:{max((content_length[round_i]) * 0.03 * font_size_eff, 5.0)}em" ' \
                  + f'class="unsortable"|{str(round_i + 1).zfill(2)}回戦'
    result += "\n"
    current_info_round_num = 0
    for in_list in in_list_list:
        info = in_list[7]
        if info is not None:
            current_info_round_num = max(current_info_round_num, info.round_num)
        bgcolor = ""
        detail_str = ""
        status = in_list[6]
        if status == "challenge":
            bgcolor = "80FF80"
            detail_str = "挑戦"
        elif status == "normal" or status == "":
            bgcolor = "F8F8F8"
        elif status == "playoff":
            bgcolor = "D0FFA0"
            detail_str = "プレーオフ"
        elif status == "downgrade":
            bgcolor = "FFA0A0"
            detail_str = "陷落" if in_list[5] != 0 else "休場·陷落"
        result += f'|-style="background-color:#{bgcolor}; height:2em"\n'
        result += f'!{in_list[1]}\n|'
        result += f'{in_list[2]}'
        result += f'||{in_list[4]}'
        result += f'||{in_list[5]}'
        result += f'||{detail_str}'
        for k in range(current_info_round_num):
            result += f'||{info.output_details[k] if (info is not None) and (k < len(info.output_details)) else " "}'
        result += "\n"
    result += '|}\n'
    return result


def kiou_title_playoff(iteration_int: int):
    iteration_str = f"第{str(iteration_int).zfill(2)}期"
    # 五番勝負
    title_matches = sql_read.read_match("棋王戦", iteration_str, "決勝リーグ戦", "プレーオフ")
    org_tree_title = organized_tr.OrganizedTree(title_matches, f"決勝リーグ戦プレーオフ", ["", ])
    if iteration_int == 1:
        return title_match.title_match_str_plus(org_tree_title,
                                                "棋王戦",
                                                iteration_str,
                                                "棋王",
                                                f"決勝リーグ戦プレーオフ",
                                                None), kishi_data.query_kishi_from_name("大内延介")
    else:
        return None
