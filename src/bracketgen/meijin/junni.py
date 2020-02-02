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


def generate_junni_table(iteration_int: int):
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
        print(str(iteration_int),
              this_junni_info.tier,
              (f"{this_junni_info.junni}({this_junni_info.current_relegation_point})"
               if this_junni_info.current_relegation_point != 0
               else f"{this_junni_info.junni}"),
              kishi_display_name,
              display_length,
              "{{Sort|%d|%s}}" % (kishi_data.rank_to_int(this_rank[0]), this_rank[0]),
              str(this_rank[1]),
              age,
              f"{prev_wins}-{prev_losses}({prev_junni}/{prev_tier})",
              str(league_info.wins),
              str(league_info.losses),
              this_junni_info.relegation_point_added,
              this_junni_info.result,
              this_junni_info.to_fc_year,
              sep="\t"
              )
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
        print(str(iteration_int),
              this_junni_info.tier,
              (f"{this_junni_info.junni}({this_junni_info.current_relegation_point})"
               if this_junni_info.current_relegation_point != 0
               else f"{this_junni_info.junni}"),
              kishi_display_name,
              display_length,
              "{{Sort|%d|%s}}" % (kishi_data.rank_to_int(this_rank[0]), this_rank[0]),
              str(this_rank[1]),
              age,
              f"{prev_wins}-{prev_losses}({prev_junni}/{prev_tier})",
              0,
              0,
              this_junni_info.relegation_point_added,
              this_junni_info.result,
              this_junni_info.to_fc_year,
              sep="\t"
              )


def query_junni_info_by_kishi(in_kishi, source_list):
    for source in source_list:
        if source.kishi == in_kishi:
            return source
    else:
        return None
