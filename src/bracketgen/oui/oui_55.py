from bracketgen import gen_round_name
from bracketgen.oui import oui_common
from importdata import sql_read
from metastruct import organized_tr, seeds_out_in, table_feed


def oui_str_dict(iteration_int: int) -> dict:
    return_dict = dict()

    iteration_str = f"第{str(iteration_int).zfill(2)}期"

    title_result = oui_common.oui_title_matches(iteration_int)
    return_dict["T"] = title_result[0]
    new_title_flag = title_result[1]
    former_title = title_result[2]
    new_title = title_result[3]

    red_group_result = oui_common.oui_group(iteration_int, "紅")
    return_dict["RED"] = red_group_result[0]
    red_non_relegated_list = red_group_result[1]
    red_relegated_list = red_group_result[2]

    white_group_result = oui_common.oui_group(iteration_int, "白")
    return_dict["WHITE"] = white_group_result[0]
    white_non_relegated_list = white_group_result[1]
    white_relegated_list = white_group_result[2]

    # match_db_1 = sql_read.read_match("王位戦", iteration_str, "予選")
    # round_db_1 = gen_round_name.read_round("王位戦", iteration_str, "予選")
    # feed_1 = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_1,
    #                                                          "予選",
    #                                                          round_db_1),
    #                               "",
    #                               "王位戦",
    #                               iteration_str,
    #                               True,
    #                               True,
    #                               "◎",
    #                               "")
    # 
    # promoted_to_group_dict = dict()
    # for node in feed_1.tree.last_remain_nodes:
    #     promoted_to_group_dict[node.winner().id] = "リーグ入り"
    # seeds_out_in.Seed(5, [feed_1.tree, ], [], [], [], promoted_to_group_dict)
    # 
    # return_dict[4] = table_feed.draw_table_from_feed([feed_1, ])
    # 
    red_non_relegated_str = ""
    for non_relegated in red_non_relegated_list:
        red_non_relegated_str += non_relegated.get_full_wiki_name()[0]
        if non_relegated != red_non_relegated_list[-1]:
            red_non_relegated_str += " / "
    red_relegated_str = ""
    for relegated in red_relegated_list:
        red_relegated_str += relegated.get_full_wiki_name()[0]
        if relegated != red_relegated_list[-1]:
            red_relegated_str += " / "
    white_non_relegated_str = ""
    for non_relegated in white_non_relegated_list:
        white_non_relegated_str += non_relegated.get_full_wiki_name()[0]
        if non_relegated != white_non_relegated_list[-1]:
            white_non_relegated_str += " / "
    white_relegated_str = ""
    for relegated in white_relegated_list:
        white_relegated_str += relegated.get_full_wiki_name()[0]
        if relegated != white_relegated_list[-1]:
            white_relegated_str += " / "

    min_match_date = sql_read.read_match_min_max_date("王位戦", iteration_str, "MIN")[0]
    max_match_date = sql_read.read_match_min_max_date("王位戦", iteration_str, "MAX")[0]

    return_dict["INFOBOX"] = (
        "{{Infobox 各年の棋戦\n"
        + f"|期=第{iteration_int}期\n"
        + "|イベント名称=王位戦\n"
        + f"|開催期間={min_match_date.isoformat()} - {max_match_date.isoformat()}\n"
        + "|タイトル=王位\n"
        + (f"|前タイトル={former_title.get_full_wiki_name()[0]}\n"
           if not new_title_flag
           else "")
        + f"|今期=第{iteration_int}期\n"
        + f"|新タイトル={new_title.get_full_wiki_name()[0]}\n"
        + "|△昇級△=\n"
        + "|▼降級▼=\n"
        + "|リーグ=リーグ\n"
        + f"|紅組残留={red_non_relegated_str}\n"
        + f"|白組残留={white_non_relegated_str}\n"
        + f"|紅組陷落={red_relegated_str}\n"
        + f"|白組陷落={white_relegated_str}\n"
        + (f"|前回=[[第{iteration_int-1}期王位戦|第{iteration_int-1}期]]\n"
           if iteration_int != 1
           else "|前回=\n")
        + f"|次回=[[第{iteration_int + 1}期王位戦|第{iteration_int + 1}期]]\n"
        + "}}\n"
    )

    return_dict["LEAD"] = (
        f"第{iteration_int}期王位戦は、{1961+iteration_int}年度（{min_match_date.isoformat()}"
        f" - {max_match_date.isoformat()}）の[[王位戦 (将棋)|王位戦]]である。\n"
        "王位戦は将棋のタイトル戦の一つである。\n"
    )

    return return_dict
