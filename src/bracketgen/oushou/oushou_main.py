from bracketgen import gen_round_name, str_list
from bracketgen.oushou import oushou_common
from importdata import sql_read
from metastruct import organized_tr, seeds_out_in, table_feed


def oushou_str_dict(iteration_int: int) -> dict:
    return_dict = dict()
    letter_list = str_list.letter_list

    iteration_str = f"第{str(iteration_int).zfill(2)}期"

    title_result = oushou_common.oushou_title_matches(iteration_int)
    return_dict["T"] = title_result[0]
    new_title_flag = title_result[1]
    former_title = title_result[2]
    new_title = title_result[3]

    feed_league_playoffs = []
    tree_league_playoffs = oushou_common.get_playoff_tree(iteration_str, "プレーオフ")
    if tree_league_playoffs[0] is not None:
        feed_league_playoff = table_feed.TableFeed(tree_league_playoffs[0],
                                                   f"",
                                                   "王将戦",
                                                   iteration_str,
                                                   True,
                                                   True,
                                                   "◎",
                                                   "")
        feed_league_playoffs.append(feed_league_playoff)
        if tree_league_playoffs[1] is not None:  # actually never happens
            feed_league_playoff_1 = table_feed.TableFeed(tree_league_playoffs[1],
                                                         f"",
                                                         "王将戦",
                                                         iteration_str,
                                                         True,
                                                         True,
                                                         "◎",
                                                         "")
            feed_league_playoffs.append(feed_league_playoff_1)
        return_dict["PLAYOFFS"] = table_feed.draw_table_from_feed(feed_league_playoffs, "決勝")

    group_result = oushou_common.oushou_group(iteration_int)
    return_dict[0] = group_result[0]
    non_relegated_list = group_result[1]
    relegated_list = group_result[2]

    feed_remain_playoffs = []
    tree_remain_playoffs = oushou_common.get_playoff_tree(iteration_str, "残留決定戦")
    if tree_remain_playoffs[0] is not None:
        feed_remain_playoff = table_feed.TableFeed(tree_remain_playoffs[0],
                                                   "", "", "", True, True, "◇", ""
                                                   )
        feed_remain_playoffs.append(feed_remain_playoff)
        if tree_remain_playoffs[1] is not None:
            feed_remain_playoff_1 = table_feed.TableFeed(tree_remain_playoffs[1],
                                                         "===残留決定戦(1敗)===\n", "", "", True, True, "◇", ""
                                                         )
            feed_remain_playoffs.append(feed_remain_playoff_1)
        return_dict["REMAINS"] = table_feed.draw_table_from_feed(feed_remain_playoffs, "決勝")

    feed_2 = []
    tree_2 = []
    if 26 <= iteration_int <= 62:
        for i in range(1):
            match_db_2_i = sql_read.read_match("王将戦", iteration_str, "二次予選")
            if len(match_db_2_i) == 0:
                continue
            round_db_2_i = gen_round_name.read_round("王将戦", iteration_str, "二次予選")
            feed_2_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_2_i,
                                                                       "二次予選",
                                                                       round_db_2_i),
                                            f"",
                                            "王将戦",
                                            iteration_str,
                                            True,
                                            False,
                                            "◎",
                                            "")
            feed_2.append(feed_2_i)
            tree_2.append(feed_2_i.tree)
    else:
        for i in range(4):
            group_str_list = ["A組", "B組", "C組", "D組"]
            group_str = f"{str(i + 1).zfill(2)}組" if iteration_int != 16 else group_str_list[i]
            match_db_2_i = sql_read.read_match("王将戦", iteration_str, "二次予選", group_str)
            if len(match_db_2_i) == 0:
                continue
            round_db_2_i = gen_round_name.read_round("王将戦", iteration_str, "二次予選", group_str)
            feed_2_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_2_i,
                                                                       "二次予選" + group_str,
                                                                       round_db_2_i),
                                            f"==={group_str}===\n",
                                            "王将戦",
                                            iteration_str,
                                            True,
                                            False,
                                            "◎",
                                            "")
            feed_2.append(feed_2_i)
            tree_2.append(feed_2_i.tree)

    promoted_to_group_dict = dict()
    for tree in tree_2:
        for node in tree.last_remain_nodes:
            promoted_to_group_dict[node.winner().id] = "リーグ入り"
    seeds_out_in.Seed(5, tree_2, [], [], [], promoted_to_group_dict)

    feed_1 = []
    tree_1 = []
    if 26 <= iteration_int <= 63:
        for i in range(1):
            match_db_1_i = sql_read.read_match("王将戦", iteration_str, "一次予選")
            if len(match_db_1_i) == 0:
                continue
            round_db_1_i = gen_round_name.read_round("王将戦", iteration_str, "一次予選")
            feed_1_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_1_i,
                                                                       "一次予選",
                                                                       round_db_1_i),
                                            f"",
                                            "王将戦",
                                            iteration_str,
                                            True,
                                            True,
                                            "◎",
                                            "")
            feed_1.append(feed_1_i)
            tree_1.append(feed_1_i.tree)
    else:
        for i in range(11):
            group_str = f"{str(i + 1).zfill(2)}組"
            match_db_1_i = sql_read.read_match("王将戦", iteration_str, "一次予選", group_str)
            if len(match_db_1_i) == 0:
                continue
            round_db_1_i = gen_round_name.read_round("王将戦", iteration_str, "一次予選", group_str)
            feed_1_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_1_i,
                                                                       "一次予選" + group_str,
                                                                       round_db_1_i),
                                            f"==={group_str}===\n",
                                            "王将戦",
                                            iteration_str,
                                            True,
                                            True,
                                            "◎",
                                            "")
            feed_1.append(feed_1_i)
            tree_1.append(feed_1_i.tree)

    seeds_out_in.Seed(1, tree_1, tree_2, letter_list)

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

    min_match_date = sql_read.read_match_min_max_date("王将戦", iteration_str, "MIN")[0]
    max_match_date = sql_read.read_match_min_max_date("王将戦", iteration_str, "MAX")[0]

    return_dict["INFOBOX"] = (
            "{{Infobox 各年の棋戦\n"
            + f"|期=第{iteration_int}期\n"
            + "|イベント名称=王将戦\n"
            + f"|開催期間={min_match_date.isoformat()} - {max_match_date.isoformat()}\n"
            + "|タイトル=王将\n"
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
            + (f"|前回=[[第{iteration_int - 1}期王将戦|第{iteration_int - 1}期]]\n"
               if iteration_int != 1
               else "|前回=\n")
            + f"|次回=[[第{iteration_int + 1}期王将戦|第{iteration_int + 1}期]]\n"
            + "}}\n"
    )

    return_dict["LEAD"] = (
        f"第{iteration_int}期王将戦は、{1950 + iteration_int}年度（{min_match_date.isoformat()}"
        f" - {max_match_date.isoformat()}）の[[王将戦]]である。\n"
        "王将戦は将棋のタイトル戦の一つである。\n"
    )
    return return_dict
