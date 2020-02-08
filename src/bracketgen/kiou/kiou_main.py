from bracketgen import gen_round_name, str_list
from bracketgen.kiou import kiou_common
from importdata import sql_read
from metastruct import organized_tr, seeds_out_in, table_feed


def kiou_str_dict(iteration_int: int) -> dict:
    return_dict = dict()
    letter_list = str_list.letter_list
    katakana_list = str_list.katakana_list

    iteration_str = (f"第{str(iteration_int).zfill(2)}期"
                     if iteration_int != 1001
                     else f"第01回")
    iteration_str_display = (f"第{str(iteration_int)}期"
                             if iteration_int != 1001
                             else f"第1回")
    iteration_str_prev = (f"第{str(iteration_int - 1)}期"
                          if iteration_int != 1
                          else f"第1回")
    iteration_str_next = (f"第{str(iteration_int + 1)}期"
                          if iteration_int != 1001
                          else f"第1期")

    if iteration_int >= 2:
        title_result = kiou_common.kiou_title_matches(iteration_int)
        return_dict["T"] = title_result[0]
        new_title_flag = title_result[1]
        former_title = title_result[2]
        new_title = title_result[3]
    elif iteration_int == 1:
        title_playoff = kiou_common.kiou_title_playoff(iteration_int)
        return_dict["T"] = title_playoff[0][0]
        return_dict["TP"] = kiou_common.kiou_title_group(iteration_int)
        new_title_flag = True
        former_title = None
        new_title = title_playoff[1]
    else:
        new_title_flag = True
        former_title = None
        new_title = None

    feed_0 = []
    tree_0 = []
    main_tournament_name = "挑戦者決定トーナメント"
    for i in range(1):
        match_db_0_i = sql_read.read_match("棋王戦", iteration_str, main_tournament_name, "")
        match_db_0_i += sql_read.read_match("棋王戦", iteration_str, main_tournament_name, "勝者組")
        round_db_0_i_winners = gen_round_name.read_round("棋王戦", iteration_str, main_tournament_name, "勝者組")
        round_db_0_i = []
        for round_0 in round_db_0_i_winners:
            round_db_0_i.append("勝者組" + round_0)
        round_db_0_i += gen_round_name.read_round("棋王戦", iteration_str, main_tournament_name, "")
        feed_0_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_0_i,
                                                                   main_tournament_name,
                                                                   round_db_0_i),
                                        f"",
                                        "棋王戦",
                                        iteration_str,
                                        False,
                                        False,
                                        "◎",
                                        "")
        feed_0.append(feed_0_i)
        tree_0.append(feed_0_i.tree)

    feed_9 = []
    tree_9 = []
    for i in range(1):
        match_db_9_i = sql_read.read_match("棋王戦", iteration_str, main_tournament_name, "敗者復活戦")
        round_db_9_i = gen_round_name.read_round("棋王戦", iteration_str, main_tournament_name, "敗者復活戦")
        feed_9_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_9_i,
                                                                   main_tournament_name + "敗者復活戦",
                                                                   round_db_9_i),
                                        f"",
                                        "棋王戦",
                                        iteration_str,
                                        True,
                                        False,
                                        "◎",
                                        "")
        feed_9.append(feed_9_i)
        tree_9.append(feed_9_i.tree)

    winner_winners_group = tree_0[0].get_winners()[0]

    seeds_out_in.Seed(-1, tree_0, tree_9, letter_list)
    if iteration_int >= 2:
        detail2_str = "挑戦者決定二番勝負" if iteration_int >= 18 else "挑戦者決定戦"
        feed_decisive = []
        tree_decisive = []
        match_db_decisive = sql_read.read_match("棋王戦", iteration_str, main_tournament_name, detail2_str)
        round_db_decisive = gen_round_name.read_round("棋王戦", iteration_str, main_tournament_name, detail2_str)
        org_tree_db_decisive = organized_tr.OrganizedTree(match_db_decisive,
                                                          main_tournament_name + detail2_str,
                                                          round_db_decisive)
        if iteration_int >= 18:
            org_tree_db_decisive.node_groups[0][0].set_1win_advantage(winner_winners_group)
        feed_decisive_i = table_feed.TableFeed(org_tree_db_decisive,
                                               (f"==挑戦者決定戦==\n"
                                                + (f"全勝進出者のアドバンテージとして☆を付記。\n"
                                                   if iteration_int >= 18
                                                   else "")
                                                ),
                                               "棋王戦",
                                               iteration_str,
                                               False,
                                               False,
                                               "◎",
                                               "")
        feed_decisive.append(feed_decisive_i)
        tree_decisive.append(feed_decisive_i.tree)
        seeds_out_in.Seed(1, tree_0, tree_decisive, ["全勝通過", ])
        seeds_out_in.Seed(1, tree_9, tree_decisive, ["敗者復活", ])

        challenge_dict = dict()
        for tree in tree_decisive:
            for node in tree.last_remain_nodes:
                challenge_dict[node.winner().id] = "挑戦者"
        seeds_out_in.Seed(5, tree_decisive, [], [], [], challenge_dict)

        return_dict["DECISIVE"] = table_feed.draw_table_from_feed(feed_decisive)

    feed_2 = []
    tree_2 = []
    if 7 <= iteration_int <= 39 and not (27 <= iteration_int <= 28):
        for i in range(1):
            match_db_2_i = sql_read.read_match("棋王戦", iteration_str, "予選")
            if len(match_db_2_i) == 0:
                continue
            round_db_2_i = gen_round_name.read_round("棋王戦", iteration_str, "予選")
            feed_2_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_2_i,
                                                                       "予選",
                                                                       round_db_2_i),
                                            f"",
                                            "棋王戦",
                                            iteration_str,
                                            True,
                                            True,
                                            "◎",
                                            "")
            feed_2.append(feed_2_i)
            tree_2.append(feed_2_i.tree)
        seeds_out_in.Seed(1, tree_2, tree_0, katakana_list)
    elif iteration_int >= 40 or (27 <= iteration_int <= 28):
        for i in range(8):
            group_str = f"{str(i + 1).zfill(2)}組"
            match_db_2_i = sql_read.read_match("棋王戦", iteration_str, "予選", group_str)
            if len(match_db_2_i) == 0:
                continue
            round_db_2_i = gen_round_name.read_round("棋王戦", iteration_str, "予選", group_str)
            feed_2_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_2_i,
                                                                       "予選" + group_str,
                                                                       round_db_2_i),
                                            f"==={group_str}===\n",
                                            "棋王戦",
                                            iteration_str,
                                            True,
                                            True,
                                            "◎",
                                            "")
            feed_2.append(feed_2_i)
            tree_2.append(feed_2_i.tree)
        seeds_out_in.Seed(1, tree_2, tree_0, katakana_list)
    else:  # 名棋戦
        meiki_iteration_str = f"第{str(iteration_int + 1).zfill(2)}回"
        meiki_iteration_str_display = f"第{str(iteration_int + 1)}回"
        for i in range(1):
            match_db_2_i = sql_read.read_match("名棋戦", meiki_iteration_str, "トーナメント戦")
            if len(match_db_2_i) == 0:
                continue
            round_db_2_i = gen_round_name.read_round("名棋戦", meiki_iteration_str, "トーナメント戦")
            feed_2_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_2_i,
                                                                       "トーナメント戦",
                                                                       round_db_2_i),
                                            (f"==={meiki_iteration_str_display}名棋戦===\n"
                                             f"準々決勝以上８名は{iteration_str_display}棋王戦出場\n"),
                                            "名棋戦",
                                            meiki_iteration_str,
                                            False,
                                            True,
                                            "◎",
                                            "")
            feed_2.append(feed_2_i)
            tree_2.append(feed_2_i.tree)
        seeds_out_in.Seed(-1, tree_2, tree_0, katakana_list[0:7])
        seeds_out_in.Seed(1, tree_2, tree_0, katakana_list[7:8])
    #
    # seeds_out_in.Seed(1, tree_1, tree_2, katakana_list)
    # seeds_out_in.Seed(1, tree_2, tree_0, letter_list)
    #
    return_dict["WINNERS"] = table_feed.draw_table_from_feed(feed_0)
    return_dict["LOSERS"] = table_feed.draw_table_from_feed(feed_9)
    return_dict["PRELIMINARY"] = table_feed.draw_table_from_feed(feed_2)
    # return_dict[1] = table_feed.draw_table_from_feed(feed_1)

    min_match_date = sql_read.read_match_min_max_date("棋王戦", iteration_str, "MIN")[0]
    max_match_date = sql_read.read_match_min_max_date("棋王戦", iteration_str, "MAX")[0]

    return_dict["INFOBOX"] = (
            "{{Infobox 各年の棋戦\n"
            + f"|期={iteration_str_display}\n"
            + "|イベント名称=棋王戦\n"
            + f"|開催期間={min_match_date.isoformat()} - {max_match_date.isoformat()}\n"
            + "|タイトル=棋王\n"
            + (f"|前タイトル={former_title.get_full_wiki_name()[0]}\n"
               if not new_title_flag
               else "")
            + f"|今期={iteration_str_display}\n"
            + f"|新タイトル={new_title.get_full_wiki_name()[0] if iteration_int != 1001 else '内藤國雄'}\n"
            + "|△昇級△=\n"
            + "|▼降級▼=\n"
            + f"|前回=[[{iteration_str_prev}棋王戦|{iteration_str_prev}]]\n"
            + f"|次回=[[{iteration_str_next}棋王戦|{iteration_str_next}]]\n"
            + "}}\n"
    )

    return_dict["LEAD"] = (
            f"{iteration_str_display}棋王戦は、{1974 + iteration_int}年度（{min_match_date.isoformat()}"
            f" - {max_match_date.isoformat()}）の[[棋王戦 (将棋)|棋王戦]]である。\n"
            + ("棋王戦は将棋のタイトル戦の一つである。\n" if iteration_int >= 1 else "")
    )

    return return_dict
