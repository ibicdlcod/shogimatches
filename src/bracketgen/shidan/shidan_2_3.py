from bracketgen import gen_round_name, str_list
from bracketgen.shidan import shidan_common
from importdata import sql_read
from metastruct import organized_tr, seeds_out_in, table_feed


def shidan_str_dict(iteration_int: int) -> dict:
    return_dict = dict()
    hiragana_list = str_list.hiragana_list

    iteration_str = f"第{str(iteration_int).zfill(2)}期"

    title_result = shidan_common.shidan_title_matches(iteration_int)
    return_dict[7] = title_result[0]
    new_title_flag = title_result[1]
    former_title = title_result[2]
    new_title = title_result[3]

    group_result = shidan_common.shidan_group(iteration_int)
    return_dict[0] = group_result[0]
    non_relegated_list = group_result[1]
    relegated_list = group_result[2]

    feed_2 = []
    tree_2 = []
    second_qualifying_groups = 2
    if iteration_int == 2:
        second_qualifying_groups = 3
    for i in range(second_qualifying_groups):
        group_str = f"{str(i + 1).zfill(2)}組"
        match_db_2_i = sql_read.read_match("十段戦", iteration_str, "二次予選", group_str)
        round_db_2_i = gen_round_name.read_round("十段戦", iteration_str, "二次予選", group_str)
        feed_2_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_2_i,
                                                                   "二次予選" + group_str,
                                                                   round_db_2_i),
                                        f"==={group_str}===\n",
                                        "十段戦",
                                        iteration_str,
                                        True,
                                        False,
                                        "◎",
                                        "")
        feed_2.append(feed_2_i)
        tree_2.append(feed_2_i.tree)

    feed_1 = []
    tree_1 = []
    for i in range(6):
        group_str = f"{str(i + 1).zfill(2)}組"
        match_db_1_i = sql_read.read_match("十段戦", iteration_str, "一次予選", group_str)
        round_db_1_i = gen_round_name.read_round("十段戦", iteration_str, "一次予選", group_str)
        feed_1_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_1_i,
                                                                   "一次予選" + group_str,
                                                                   round_db_1_i),
                                        f"==={group_str}===\n",
                                        "十段戦",
                                        iteration_str,
                                        True,
                                        True,
                                        "◎",
                                        "")
        feed_1.append(feed_1_i)
        tree_1.append(feed_1_i.tree)
    seeds_out_in.Seed(1, tree_1, tree_2, hiragana_list)
    promoted_to_group_dict = dict()
    for tree in tree_2:
        for node in tree.last_remain_nodes:
            promoted_to_group_dict[node.winner().id] = "リーグ入り"
    seeds_out_in.Seed(5, tree_2, [], [], [], promoted_to_group_dict)

    return_dict[2] = table_feed.draw_table_from_feed(feed_2)
    return_dict[1] = table_feed.draw_table_from_feed(feed_1)

    non_relegated_str = ""
    for non_relegated in non_relegated_list:
        non_relegated_str += non_relegated.get_full_wiki_name()[0]
        if non_relegated != non_relegated_list[-1]:
            non_relegated_str += " / "
    relegated_str = ""
    for relegated in relegated_list:
        relegated_str += relegated.get_full_wiki_name()[0]
        if relegated != relegated_list[-1]:
            relegated_str += " / "

    min_match_date = sql_read.read_match_min_max_date("十段戦", iteration_str, "MIN")[0]
    max_match_date = sql_read.read_match_min_max_date("十段戦", iteration_str, "MAX")[0]

    return_dict["INFOBOX"] = (
            "{{Infobox 各年の棋戦\n"
            + f"|期=第{iteration_int}期\n"
            + "|イベント名称=十段戦\n"
            + f"|開催期間={min_match_date.isoformat()} - {max_match_date.isoformat()}\n"
            + "|タイトル=十段\n"
            + (f"|前タイトル={former_title.get_full_wiki_name()[0]}\n"
               if not new_title_flag
               else "")
            + f"|今期=第{iteration_int}期\n"
            + f"|新タイトル={new_title.get_full_wiki_name()[0]}\n"
            + "|△昇級△=\n"
            + "|▼降級▼=\n"
            + "|リーグ=リーグ\n"
            + f"|リーグ残留={non_relegated_str}\n"
            + f"|リーグ陷落={relegated_str}\n"
            + (f"|前回=[[第{iteration_int - 1}期十段戦|第{iteration_int - 1}期]]\n"
               if iteration_int != 1
               else "|前回=[[第12期九段戦]]\n")
            + (f"|次回=[[第{iteration_int + 1}期十段戦|第{iteration_int + 1}期]]\n"
               if iteration_int != 26
               else "|次回=[[第1期竜王戦]]\n")
            + "}}\n"
    )

    return_dict["LEAD"] = (
        f"第{iteration_int}期十段戦は、{1961 + iteration_int}年度（{min_match_date.isoformat()}"
        f" - {max_match_date.isoformat()}）の[[十段戦 (将棋)|十段戦]]である。\n"
        "十段戦は将棋のタイトル戦の一つである。\n"
    )

    return return_dict
