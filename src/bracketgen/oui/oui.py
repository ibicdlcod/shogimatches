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

    feeds_playoffs = []
    if iteration_int != 1:
        feed_inter_league = table_feed.TableFeed(oui_common.get_playoff_tree(iteration_str, "挑戦者決定戦"),
                                                 "===挑戦者決定戦===\n",
                                                 "王位戦",
                                                 iteration_str,
                                                 True,
                                                 True,
                                                 "◎",
                                                 "")
        feeds_playoffs.append(feed_inter_league)
    red_po_tree = oui_common.get_playoff_tree(iteration_str, "紅組プレーオフ")
    if red_po_tree is not None:
        feed_red_po = table_feed.TableFeed(red_po_tree, "===紅組プレーオフ===\n",
                                           "", "", True, True, "◎", ""
                                           )
        feeds_playoffs.append(feed_red_po)
    white_po_tree = oui_common.get_playoff_tree(iteration_str, "白組プレーオフ")
    if white_po_tree is not None:
        feed_white_po = table_feed.TableFeed(white_po_tree, "===白組プレーオフ===\n",
                                             "", "", True, True, "◎", ""
                                             )
        feeds_playoffs.append(feed_white_po)
    return_dict["PLAYOFFS"] = table_feed.draw_table_from_feed(feeds_playoffs, "決勝")
    if return_dict["PLAYOFFS"] == "":
        return_dict.pop("PLAYOFFS")

    red_group_result = oui_common.oui_group(iteration_int, "紅")
    return_dict["RED"] = red_group_result[0]
    red_non_relegated_list = red_group_result[1]
    red_relegated_list = red_group_result[2]

    white_group_result = oui_common.oui_group(iteration_int, "白")
    return_dict["WHITE"] = white_group_result[0]
    white_non_relegated_list = white_group_result[1]
    white_relegated_list = white_group_result[2]

    feeds_remain_playoffs = []
    red_remain_po_tree = oui_common.get_playoff_tree(iteration_str, "紅組残留決定戦")
    if red_remain_po_tree is not None:
        feed_remain_red_po = table_feed.TableFeed(red_remain_po_tree, "===紅組残留決定戦===\n",
                                                  "", "", True, True, "◎", ""
                                                  )
        feeds_remain_playoffs.append(feed_remain_red_po)
    white_remain_po_tree = oui_common.get_playoff_tree(iteration_str, "白組残留決定戦")
    if white_remain_po_tree is not None:
        feed_remain_white_po = table_feed.TableFeed(white_remain_po_tree, "===白組残留決定戦===\n",
                                                    "", "", True, True, "◎", ""
                                                    )
        feeds_remain_playoffs.append(feed_remain_white_po)
    return_dict["REMAINS"] = table_feed.draw_table_from_feed(feeds_remain_playoffs, "決勝")
    if return_dict["REMAINS"] == "":
        return_dict.pop("REMAINS")

    feed_1 = []
    tree_1 = []
    if iteration_int >= 55 or iteration_int <= 18:
        for i in range(10):
            group_str = f"{str(i + 1).zfill(2)}組"
            match_db_1_i = sql_read.read_match("王位戦", iteration_str, "予選", group_str)
            if len(match_db_1_i) == 0:
                continue
            round_db_1_i = gen_round_name.read_round("王位戦", iteration_str, "予選", group_str)
            feed_1_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_1_i,
                                                                       "予選" + group_str,
                                                                       round_db_1_i),
                                            f"==={group_str}===\n",
                                            "王位戦",
                                            iteration_str,
                                            True,
                                            True,
                                            "◎",
                                            "")
            feed_1.append(feed_1_i)
            tree_1.append(feed_1_i.tree)
    else:
        match_db_1_i = sql_read.read_match("王位戦", iteration_str, "予選")
        round_db_1_i = gen_round_name.read_round("王位戦", iteration_str, "予選")
        feed_1_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_1_i,
                                                                   "予選",
                                                                   round_db_1_i),
                                        f"",
                                        "王位戦",
                                        iteration_str,
                                        True,
                                        True,
                                        "◎",
                                        "")
        feed_1.append(feed_1_i)
        tree_1.append(feed_1_i.tree)
    promoted_to_group_dict = dict()
    for tree in tree_1:
        for node in tree.last_remain_nodes:
            promoted_to_group_dict[node.winner().id] = "リーグ入り"
    seeds_out_in.Seed(5, tree_1, [], [], [], promoted_to_group_dict)
    return_dict["PRELIMINARY"] = table_feed.draw_table_from_feed(feed_1)

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
            + (f"|前回=[[第{iteration_int - 1}期王位戦|第{iteration_int - 1}期]]\n"
               if iteration_int != 1
               else "|前回=\n")
            + f"|次回=[[第{iteration_int + 1}期王位戦|第{iteration_int + 1}期]]\n"
            + "}}\n"
    )

    return_dict["LEAD"] = (
        f"第{iteration_int}期王位戦は、{1961 + iteration_int}年度（{min_match_date.isoformat()}"
        f" - {max_match_date.isoformat()}）の[[王位戦 (将棋)|王位戦]]である。\n"
        "王位戦は将棋のタイトル戦の一つである。\n"
    )

    return return_dict
