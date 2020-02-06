from bracketgen import lea_from_mat, title_match, gen_round_name
from importdata import sql_read
from metastruct import junni_info_generic, organized_tr


def oui_title_matches(iteration_int: int):
    iteration_str = f"第{str(iteration_int).zfill(2)}期"
    iteration_str_prev = f"第{str(iteration_int - 1).zfill(2)}期"
    # 七番勝負
    title_matches = sql_read.read_match("王位戦", iteration_str, "タイトル戦", "七番勝負")
    if iteration_int != 1:
        title_matches_last = sql_read.read_match("王位戦", iteration_str_prev, "タイトル戦", "七番勝負")
        org_tree_title_last = organized_tr.OrganizedTree(title_matches_last, f"タイトル戦七番勝負", ["", ])
    else:
        org_tree_title_last = None
    org_tree_title = organized_tr.OrganizedTree(title_matches, f"タイトル戦七番勝負", ["", ])
    return title_match.title_match_str_plus(org_tree_title,
                                            "王位戦",
                                            iteration_str,
                                            "王位",
                                            "七番勝負",
                                            org_tree_title_last)


def oui_group(iteration_int: int, red_or_white: str):
    result_list_list = []

    junni_info_list = junni_info_generic.junni_info_from_sql("王位戦", iteration_int)
    junni_info_dict = dict()
    junni_info_full_dict = dict()
    junni_result_dict = dict()
    for junni_info_item in junni_info_list:
        junni_info_dict[junni_info_item.kishi.id] = junni_info_item.junni
        junni_info_full_dict[junni_info_item.kishi.id] = junni_info_item
        junni_result_dict[junni_info_item.kishi] = junni_info_item.result

    iteration_str = f"第{str(iteration_int).zfill(2)}期"
    junni_matches = sql_read.read_match("王位戦", iteration_str, "挑戦者決定リーグ", red_or_white + "組")
    league_info_db = lea_from_mat.gen_lea_pos_no_round_names(junni_matches, junni_info_dict)

    participants = []
    for league_info in league_info_db:
        participants.append(league_info.kishi)
        this_id = league_info.kishi.id
        this_junni_info = junni_info_full_dict[this_id]
        this_kishi = league_info.kishi
        last_match_date = league_info.last_match_date
        this_rank = this_kishi.rank(last_match_date)
        display_length = len(this_kishi.fullname)
        if this_kishi.wiki_name == "":
            kishi_display_name = ("[["
                                  + this_kishi.fullname
                                  + "]]")
        else:
            kishi_display_name = ("[["
                                  + this_kishi.wiki_name
                                  + "|"
                                  + this_kishi.fullname
                                  + "]]")
        result_list_list.append([
            iteration_int,
            f"{this_junni_info.junni}" if 27 <= iteration_int <= 55 else "",
            kishi_display_name + this_rank[0],
            display_length + this_rank[1],
            league_info.wins,
            league_info.losses,
            this_junni_info.result,
            league_info,
            this_id,
        ])
    result = draw_table_oui_group(result_list_list)

    relegated_list = []
    non_relegated_list = []
    for k, v in junni_result_dict.items():
        if k not in participants:
            continue
        else:
            if v == "downgrade":
                relegated_list.append(k)
            else:
                non_relegated_list.append(k)
    return result, non_relegated_list, relegated_list


def draw_table_oui_group(in_list_list: list):
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

    result += f"挑決1名・陷落{relegated_num}名\n"

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
            detail_str = "挑決"
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


def get_playoff_tree(iteration: str, playoff_desc: str):
    match_db = sql_read.read_match("王位戦", iteration, "挑戦者決定リーグ", playoff_desc)
    if len(match_db) == 0:
        return None
    round_db = gen_round_name.read_round("王位戦", iteration, "挑戦者決定リーグ", playoff_desc)
    org_tree = organized_tr.OrganizedTree(match_db, f"挑戦者決定リーグ{playoff_desc}", round_db)
    return org_tree
