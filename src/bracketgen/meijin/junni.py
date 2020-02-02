from bracketgen import gen_round_name, lea_from_mat
from importdata import sql_read
from metastruct import junni_info, kishi_data

win_dicts_dict = {}
loss_dicts_dict = {}
for i in range(7, 78):
    if i in range(31, 36):
        continue
    win_dicts_dict[i] = dict()
    loss_dicts_dict[i] = dict()


def generate_junni_table(iteration_int: int):
    iteration_str = f"第{str(iteration_int).zfill(2)}期"
    junni_info_list = junni_info.junni_info_from_sql(iteration_int)
    junni_info_list_prev = junni_info.junni_info_from_sql(iteration_int - 1)
    junni_info_dict = dict()
    junni_info_full_dict = dict()
    junni_info_dict_prev = dict()
    junni_tier_dict_prev = dict()
    for junni_info_item in junni_info_list:
        junni_info_dict[junni_info_item.kishi.id] = junni_info_item.junni
        junni_info_full_dict[junni_info_item.kishi.id] = junni_info_item
    for junni_info_item in junni_info_list_prev:
        junni_info_dict_prev[junni_info_item.kishi.id] = junni_info_item.junni
        junni_tier_dict_prev[junni_info_item.kishi.id] = junni_info_item.tier

    junni_matches_c2 = sql_read.read_match("順位戦", iteration_str, "C級2組")
    junni_round_c2 = gen_round_name.read_round("順位戦", iteration_str, "C級2組", league=True)
    league_info_db_c2 = lea_from_mat.generate_lea_pos(junni_matches_c2, junni_info_dict, junni_round_c2, "C級2組")

    for league_info in league_info_db_c2:
        this_id = league_info.kishi.id
        print(junni_info_full_dict[this_id].junni,
              league_info.kishi.fullname,
              league_info.kishi.rank(league_info.last_match_date)[0],
              league_info.kishi.rank(league_info.last_match_date)[1],
              kishi_data.rank_to_int(league_info.kishi.rank(league_info.last_match_date)[0]),
              win_dicts_dict[iteration_int-1][this_id] if this_id in win_dicts_dict[iteration_int-1] else 0,
              loss_dicts_dict[iteration_int-1][this_id] if this_id in loss_dicts_dict[iteration_int-1] else 0,
              junni_info_dict_prev[this_id] if this_id in junni_info_dict_prev.keys() else 0,
              junni_tier_dict_prev[this_id] if this_id in junni_tier_dict_prev.keys() else "N",
              league_info.wins,
              league_info.losses,
              junni_info_full_dict[this_id].result
              )
        win_dicts_dict[iteration_int][this_id] = league_info.wins
        loss_dicts_dict[iteration_int][this_id] = league_info.losses


def query_junni_info_by_kishi(in_kishi, source_list):
    for source in source_list:
        if source.kishi == in_kishi:
            return source
    else:
        return None
