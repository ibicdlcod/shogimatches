from datetime import date
from bracketgen import gen_round_name, lea_from_mat
from importdata import sql_read
from metastruct import junni_info, kishi_data
from dateutil.relativedelta import relativedelta

win_dicts_dict = {}
loss_dicts_dict = {}
for i in range(7, 78):
    if i in range(31, 36):
        continue
    win_dicts_dict[i] = dict()
    loss_dicts_dict[i] = dict()


def generate_junni_table(iteration_int: int, write: bool):
    result_list_list = []

    iteration_str = f"第{str(iteration_int).zfill(2)}期"
    iteration_int_prev = (iteration_int - 1) if iteration_int != 36 else 30
    junni_info_list = junni_info.junni_info_from_sql(iteration_int)
    junni_info_list_prev = junni_info.junni_info_from_sql(iteration_int_prev)
    junni_info_dict = dict()
    junni_info_full_dict = dict()
    junni_junni_dict_prev = dict()
    junni_tier_dict_prev = dict()
    for junni_info_item in junni_info_list:
        junni_info_dict[junni_info_item.kishi.id] = junni_info_item.junni
        junni_info_full_dict[junni_info_item.kishi.id] = junni_info_item
    for junni_info_item in junni_info_list_prev:
        junni_junni_dict_prev[junni_info_item.kishi.id] = junni_info_item.junni
        junni_tier_dict_prev[junni_info_item.kishi.id] = junni_info_item.tier

    junni_matches_a = sql_read.read_match("順位戦", iteration_str, "A級", "")
    junni_round_a = gen_round_name.read_round("順位戦", iteration_str, "A級", "", league=True)
    junni_matches_a_other = sql_read.read_match("順位戦", iteration_str, "A級", "順位決定持将棋指し直し")
    if len(junni_matches_a_other) > 0:
        for match in junni_matches_a_other:
            match.detail2 = ""
        junni_matches_a += junni_matches_a_other
    league_info_db_a = lea_from_mat.generate_lea_pos(junni_matches_a, junni_info_dict, junni_round_a, "A級")

    junni_matches_b1 = sql_read.read_match("順位戦", iteration_str, "B級1組")
    junni_round_b1 = gen_round_name.read_round("順位戦", iteration_str, "B級1組", league=True)
    league_info_db_b1 = lea_from_mat.generate_lea_pos(junni_matches_b1, junni_info_dict, junni_round_b1, "B級1組")

    junni_matches_b2 = sql_read.read_match("順位戦", iteration_str, "B級2組")
    junni_round_b2 = gen_round_name.read_round("順位戦", iteration_str, "B級2組", league=True)
    if "順位決定持将棋指し直し" in junni_round_b2:
        junni_round_b2 = ["", ]
        junni_matches_b2 = sql_read.read_match("順位戦", iteration_str, "B級2組", "")
        junni_matches_b2_other = sql_read.read_match("順位戦", iteration_str, "B級2組", "順位決定持将棋指し直し")
        for match in junni_matches_b2_other:
            match.detail2 = ""
        junni_matches_b2 += junni_matches_b2_other
    league_info_db_b2 = lea_from_mat.generate_lea_pos(junni_matches_b2, junni_info_dict, junni_round_b2, "B級2組")

    junni_matches_c1 = sql_read.read_match("順位戦", iteration_str, "C級1組")
    junni_round_c1 = gen_round_name.read_round("順位戦", iteration_str, "C級1組", league=True)
    if "順位決定持将棋指し直し" in junni_round_c1:
        junni_round_c1 = ["", ]
        junni_matches_c1 = sql_read.read_match("順位戦", iteration_str, "C級1組", "")
        junni_matches_c1_other = sql_read.read_match("順位戦", iteration_str, "C級1組", "順位決定持将棋指し直し")
        for match in junni_matches_c1_other:
            match.detail2 = ""
        junni_matches_c1 += junni_matches_c1_other
    league_info_db_c1 = lea_from_mat.generate_lea_pos(junni_matches_c1, junni_info_dict, junni_round_c1, "C級1組")

    junni_matches_c2 = sql_read.read_match("順位戦", iteration_str, "C級2組")
    junni_round_c2 = gen_round_name.read_round("順位戦", iteration_str, "C級2組", league=True)
    if "三位決定戦" in junni_round_c2:
        junni_round_c2 = ["", ]
        junni_matches_c2 = sql_read.read_match("順位戦", iteration_str, "C級2組", None, "")
    league_info_db_c2 = lea_from_mat.generate_lea_pos(junni_matches_c2, junni_info_dict, junni_round_c2, "C級2組")

    league_info_db = (league_info_db_a
                      + league_info_db_b1
                      + league_info_db_b2
                      + league_info_db_c1
                      + league_info_db_c2
                      )
    junni_participants = [info.kishi for info in junni_info_list]
    last_match_date_all = date.fromisoformat("1900-01-01")
    for league_info in league_info_db:
        this_id = league_info.kishi.id
        this_junni_info = junni_info_full_dict[this_id]
        this_kishi = league_info.kishi
        junni_participants.remove(this_kishi)
        last_match_date = league_info.last_match_date
        last_match_date_all = max(last_match_date, last_match_date_all)
        this_rank = this_kishi.rank(last_match_date)
        prev_wins = (win_dicts_dict[iteration_int_prev][this_id]
                     if this_id in win_dicts_dict[iteration_int_prev].keys() else 0)
        prev_losses = (loss_dicts_dict[iteration_int_prev][this_id]
                       if this_id in loss_dicts_dict[iteration_int_prev].keys() else 0)
        prev_junni = junni_junni_dict_prev[this_id] if this_id in junni_junni_dict_prev.keys() else 0
        prev_tier = junni_tier_dict_prev[this_id] if this_id in junni_tier_dict_prev.keys() else "N"
        age = (str(relativedelta(last_match_date, this_kishi.birthday()).years)
               if this_kishi.birthday is not None
               else "不明")
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
        if prev_tier == "M":
            former_result_string = "前名人"
        elif prev_tier == "FC":
            former_result_string = "フリークラス"
        elif prev_tier == "N":
            former_result_string = "未参加"
        else:
            former_result_string = f"{prev_wins}-{prev_losses}({prev_junni}/{prev_tier})"
        result_list_list.append([
            iteration_int,
            this_junni_info.tier,
            (f"{this_junni_info.junni}({this_junni_info.current_relegation_point})"
             if this_junni_info.current_relegation_point != 0
             else f"{this_junni_info.junni}"),
            kishi_display_name,
            display_length,
            "{{Sort|%d|%s}}" % (kishi_data.rank_to_int(this_rank[0]), this_rank[0]),
            this_rank[1],
            age,
            former_result_string,
            league_info.wins,
            league_info.losses,
            this_junni_info.current_relegation_point,
            this_junni_info.relegation_point_added,
            this_junni_info.result,
            this_junni_info.to_fc_year,
            league_info,
        ])
        win_dicts_dict[iteration_int][this_id] = league_info.wins
        loss_dicts_dict[iteration_int][this_id] = league_info.losses
    for this_kishi in junni_participants:
        this_id = this_kishi.id
        this_junni_info = junni_info_full_dict[this_id]
        display_length = len(this_kishi.fullname)
        this_rank = this_kishi.rank(last_match_date_all)
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
        age = (str(relativedelta(last_match_date_all, this_kishi.birthday()).years)
               if this_kishi.birthday is not None
               else "不明")
        prev_wins = (win_dicts_dict[iteration_int_prev][this_id]
                     if this_id in win_dicts_dict[iteration_int_prev].keys() else 0)
        prev_losses = (loss_dicts_dict[iteration_int_prev][this_id]
                       if this_id in loss_dicts_dict[iteration_int_prev].keys() else 0)
        prev_junni = junni_junni_dict_prev[this_id] if this_id in junni_junni_dict_prev.keys() else 0
        prev_tier = junni_tier_dict_prev[this_id] if this_id in junni_tier_dict_prev.keys() else "N"
        if prev_tier == "M":
            former_result_string = "前名人"
        elif prev_tier == "FC":
            former_result_string = "フリークラス"
        elif prev_tier == "N":
            former_result_string = "未参加"
        else:
            former_result_string = f"{prev_wins}-{prev_losses}({prev_junni}/{prev_tier})"
        result_list_list.append([
            iteration_int,
            this_junni_info.tier,
            (f"{this_junni_info.junni}({this_junni_info.current_relegation_point})"
             if this_junni_info.current_relegation_point != 0
             else f"{this_junni_info.junni}"),
            kishi_display_name,
            display_length,
            "{{Sort|%d|%s}}" % (kishi_data.rank_to_int(this_rank[0]), this_rank[0]),
            this_rank[1],
            age,
            former_result_string,
            0,
            0,
            this_junni_info.current_relegation_point,
            this_junni_info.relegation_point_added,
            this_junni_info.result,
            this_junni_info.to_fc_year,
            None,
            ])
    result_a_list = []
    result_b1_list = []
    result_b2_list = []
    result_c1_list = []
    result_c2_list = []
    result_fc_list = []
    for result_list in result_list_list:
        if result_list[1] == "A":
            result_a_list.append(result_list)
        if result_list[1] == "B1":
            result_b1_list.append(result_list)
        if result_list[1] == "B2":
            result_b2_list.append(result_list)
        if result_list[1] == "C1":
            result_c1_list.append(result_list)
        if result_list[1] == "C2":
            result_c2_list.append(result_list)
        if result_list[1] == "FC":
            result_fc_list.append(result_list)
    result = ('{| border="1" class="wikitable" style="font-size:70%"\n'
              '|\n'
              '*{{colorbox|#80FF80}}名人挑戦または昇級 / '
              '{{colorbox|#D0FFA0}}A級プレーオフ進出 / '
              '{{colorbox|#FFA0A0}}降級\n'
              '*(順位欄){{colorbox|#FFE0E0}}降級点1回 / '
              '{{colorbox|#FFC0C0}}降級点2回（いずれも今期順位戦開始時点）\n'
              '*{{colorbox|#B0B0FF}}フリークラス転出 / '
              '{{colorbox|#FFA0D0}}降級点消去 /'
              '{{colorbox|#D0D0D0}}休場\n'
              '*{{colorbox|#FFC0A0}}引退 / '
              "{{colorbox|#A0A0A0}}死去\n"
              + ('*B級2組・C級1組は降級点2回で降級、C級2組は降級点3回で降級。\n' if iteration_int >= 17 else "")
              + '|}\n')
    result_a = draw_table_junni(result_a_list, "A", iteration_int)
    result_b1 = draw_table_junni(result_b1_list, "B1", iteration_int)
    result_b2 = draw_table_junni(result_b2_list, "B2", iteration_int)
    result_c1 = draw_table_junni(result_c1_list, "C1", iteration_int)
    result_c2 = draw_table_junni(result_c2_list, "C2", iteration_int)
    draw_table_junni_fc(result_fc_list)
    if write:
        outfile_name = f"txt_dst\\junni\\{iteration_int}.txt"
        outfile = open(outfile_name, 'w', encoding="utf-8-sig")
        outfile.write(result)
        outfile.write(result_a)
        outfile.write(result_b1)
        outfile.write(result_b2)
        outfile.write(result_c1)
        outfile.write(result_c2)
        outfile.close()
    return [result_a, result_b1, result_b2, result_c1, result_c2]


def query_junni_info_by_kishi(in_kishi, source_list):
    for source in source_list:
        if source.kishi == in_kishi:
            return source
    else:
        return None


def draw_table_junni(in_list_list: list, tier: str, iteration_int: int):
    result = ""
    relegated_num = 0
    relegated_point_num = 0
    promotion_num = 0
    max_name_length = 0
    max_rank_length = 0
    round_length = 0
    content_length = dict()
    for in_list in in_list_list:
        max_name_length = max(max_name_length, in_list[4])
        max_rank_length = max(max_rank_length, in_list[6])
        current_info_round_num = in_list[15].round_num if in_list[15] is not None else 0
        round_length = max(round_length, current_info_round_num)
        for round_j in range(current_info_round_num):
            if round_j not in content_length.keys():
                content_length[round_j] = in_list[15].output_detail_lengths[round_j]
            else:
                content_length[round_j] = max(content_length[round_j],
                                              in_list[15].output_detail_lengths[round_j])
        if iteration_int <= 16 and in_list[12] >= 1:
            relegated_num += 1
        elif iteration_int >= 17:
            if tier == "A" or tier == "B1":
                if in_list[12] >= 1:
                    relegated_num += 1
            elif tier == "B2" or tier == "C1":
                if in_list[12] + in_list[11] >= 2:
                    relegated_num += 1
            elif tier == "C2":
                if in_list[12] + in_list[11] >= 3:
                    relegated_num += 1
            if in_list[12] >= 1:
                relegated_point_num += 1
        if in_list[13] == "upgrade":
            promotion_num += 1

    if tier == "A":
        result += f"名人挑戦1名・降級{relegated_num}名\n"
    if tier == "B1":
        result += f"昇級{promotion_num}名・降級{relegated_num}名\n"
    if tier == "B2" or tier == "C1" or tier == "C2":
        if iteration_int <= 16:
            result += f"昇級{promotion_num}名・降級{relegated_num}名\n"
        else:
            result += f"昇級{promotion_num}名・降級点{relegated_point_num}名\n"
    content_size = 0
    for round_i in range(round_length):
        content_size += (content_length[round_i])
    content_size += max_name_length
    content_size += max_rank_length + 1
    font_size = 1400 / (content_size / 3 + 12)
    font_size_eff = max(50.0, font_size)
    # font_size = max(50.0, font_size)
    result += ('{|class="wikitable plainrowheaders sortable" style="text-align:center; font-size: %f%%;"\n'
               % (font_size, ))
    result += '|-\n'
    result += (f'!順位!!style="width:{max_name_length * 0.03 * font_size_eff}em" class="unsortable"|棋士名'
               f'!!style="width:{(max_rank_length + 1) * 0.02 * font_size_eff}em"|段位!!年齢!!'
               f'class="unsortable"|前期成績(順位)!!勝!!負!!class="unsortable"|備考')
    for round_i in range(round_length):
        result += f'!!style="width:{max((content_length[round_i]) * 0.03 * font_size_eff, 5.0)}em" '\
                  + f'class="unsortable"|{str(round_i+1).zfill(2)}回戦'
    result += "\n"
    current_info_round_num = 0
    for in_list in in_list_list:
        info = in_list[15]
        if info is not None:
            current_info_round_num = max(current_info_round_num, info.round_num)
        bgcolor = ""
        bgcolor0 = None
        detail_str = ""
        if in_list[11] == 1:
            bgcolor0 = "FFE0E0"
        elif in_list[11] == 2:
            bgcolor0 = "FFC0C0"
        status = in_list[13]
        if status == "challenge":
            bgcolor = "80FF80"
            detail_str = "挑戦"
        elif status == "normal":
            bgcolor = "F8F8F8"
            if in_list[12]:
                detail_str = f"降級点{in_list[11]}→{in_list[11]+1}"
            else:
                detail_str = ""
        elif status == "upgrade":
            bgcolor = "80FF80"
            detail_str = "昇級"
        elif status == "playoff":
            bgcolor = "D0FFA0"
            detail_str = "プレーオフ"
        elif status == "downgrade":
            bgcolor = "FFA0A0"
            detail_str = "降級" if in_list[10] != 0 else "休場·降級"
        elif status == "to_fc":
            bgcolor = "B0B0FF"
            detail_str = "FC転出"
        elif status == "minus_point":
            bgcolor = "FFA0D0"
            detail_str = f"降級点{in_list[11]}→{in_list[11]-1}"
        elif status == "absent":
            bgcolor = "D0D0D0"
            detail_str = "休場"
        elif status == "retire":
            bgcolor = "FFC0A0"
            detail_str = "引退"
        elif status == "dead":
            bgcolor = "A0A0A0"
            detail_str = "死去"
        result += f'|-style="background-color:#{bgcolor}; height:2em"\n'
        if bgcolor0 is None:
            result += f'!{in_list[2]}\n|'
        else:
            result += f'!style="background-color:#{bgcolor0}"|{in_list[2]}\n|'
        result += f'{in_list[3]}'
        result += f'||{in_list[5]}'
        result += f'||{in_list[7]}'
        result += f'||{in_list[8]}'
        result += f'||{in_list[9]}'
        result += f'||{in_list[10]}'
        result += f'||{detail_str}'
        for k in range(current_info_round_num):
            result += f'||{info.output_details[k] if (info is not None) and (k < len(info.output_details)) else " "}'
        result += "\n"
    result += '|}\n'
    return result


def draw_table_junni_fc(in_list_list: list):
    # for in_list in in_list_list:
    #     print(in_list)
    pass
