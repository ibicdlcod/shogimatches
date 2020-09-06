from bracketgen import gen_round_name, str_list
from bracketgen.ouza import ouza_common
from importdata import sql_read
from metastruct import organized_tr, seeds_out_in, table_feed


def ouza_str_dict(iteration_int: int) -> dict:
    return_dict = dict()
    letter_list = str_list.letter_list
    katakana_list = str_list.katakana_list

    iteration_str = (f"第{str(iteration_int).zfill(2)}期"
                     if iteration_int >= 31
                     else f"第{str(iteration_int).zfill(2)}回")
    iteration_str_display = (f"第{str(iteration_int)}期"
                             if iteration_int >= 31
                             else f"第{str(iteration_int)}回")
    iteration_str_prev = (f"第{str(iteration_int - 1)}期"
                          if iteration_int >= 32
                          else f"第{str(iteration_int - 1)}回")
    if iteration_int == 1:
        iteration_str_prev = ""
    iteration_str_next = (f"第{str(iteration_int + 1)}期"
                          if iteration_int >= 30
                          else f"第{str(iteration_int + 1)}回")

    if iteration_int >= 18:
        if iteration_int >= 31:
            title_result = ouza_common.ouza_title_matches(iteration_int)
        else:
            title_result = ouza_common.ouza_pseudo_title_matches(iteration_int)
        return_dict["T"] = title_result[0]
        new_title_flag = title_result[1]
        former_title = title_result[2]
        new_title = title_result[3]
    else:
        new_title_flag = True
        former_title = None
        new_title = None

    feed_0 = []
    tree_0 = []
    main_tournament_name = "本戦" if iteration_int < 18 else "挑戦者決定トーナメント"
    for i in range(1):
        match_db_0_i = sql_read.read_match("王座戦", iteration_str, main_tournament_name)
        round_db_0_i = gen_round_name.read_round("王座戦", iteration_str, main_tournament_name)
        feed_0_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_0_i,
                                                                   main_tournament_name,
                                                                   round_db_0_i),
                                        f"",
                                        "王座戦",
                                        iteration_str,
                                        True,
                                        False,
                                        "◎",
                                        "")
        feed_0.append(feed_0_i)
        tree_0.append(feed_0_i.tree)

    winner_name = ""
    if iteration_int < 18:
        winner_dict = dict()
        for tree in tree_0:
            for node in tree.last_remain_nodes:
                winner_dict[node.winner().id] = "優勝"
                winner_name = node.winner().get_full_wiki_name()
        seeds_out_in.Seed(5, tree_0, [], [], [], winner_dict)

    feed_2 = []
    tree_2 = []
    group_2_str_list = ["A組", "B組", "C組", "D組", "E組", "F組",
                        "G組", "H組", "I組", "J組", "K組", "L組"]
    if 4 <= iteration_int <= 25 or iteration_int >= 62:
        for i in range(12):
            if iteration_int in (list(range(4, 7)) + list(range(8, 12)) + list(range(15, 26))) \
                    or iteration_int >= 62:
                group_str = f"{str(i + 1).zfill(2)}組"
            else:
                group_str = group_2_str_list[i]
            match_db_2_i = sql_read.read_match("王座戦", iteration_str, "二次予選", group_str)
            if len(match_db_2_i) == 0:
                continue
            round_db_2_i = gen_round_name.read_round("王座戦", iteration_str, "二次予選", group_str)
            feed_2_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_2_i,
                                                                       "二次予選" + group_str,
                                                                       round_db_2_i),
                                            f"==={group_str}===\n",
                                            "王座戦",
                                            iteration_str,
                                            True,
                                            False,
                                            "◎",
                                            "")
            feed_2.append(feed_2_i)
            tree_2.append(feed_2_i.tree)
    elif iteration_int >= 4:
        for i in range(1):
            match_db_2_i = sql_read.read_match("王座戦", iteration_str, "二次予選")
            if len(match_db_2_i) == 0:
                continue
            round_db_2_i = gen_round_name.read_round("王座戦", iteration_str, "二次予選")
            feed_2_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_2_i,
                                                                       "二次予選",
                                                                       round_db_2_i),
                                            f"",
                                            "王座戦",
                                            iteration_str,
                                            True,
                                            False,
                                            "◎",
                                            "")
            feed_2.append(feed_2_i)
            tree_2.append(feed_2_i.tree)
    else:
        for i in range(5):
            group_str = f"{str(i + 1).zfill(2)}組"
            match_db_2_i = sql_read.read_match("王座戦", iteration_str, "予選", group_str)
            if len(match_db_2_i) == 0:
                continue
            round_db_2_i = gen_round_name.read_round("王座戦", iteration_str, "予選", group_str)
            feed_2_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_2_i,
                                                                       "予選" + group_str,
                                                                       round_db_2_i),
                                            f"==={group_str}===\n",
                                            "王座戦",
                                            iteration_str,
                                            True,
                                            False,
                                            "◎",
                                            "")
            feed_2.append(feed_2_i)
            tree_2.append(feed_2_i.tree)

    feed_1 = []
    tree_1 = []
    group_1_str_list = ["イ組", "ロ組", "ハ組", "ニ組", "ホ組", "ヘ組"]
    if 4 <= iteration_int <= 25 or iteration_int >= 62:
        for i in range(6):
            group_str = f"{str(i + 1).zfill(2)}組" if iteration_int <= 25 else group_1_str_list[i]
            match_db_1_i = sql_read.read_match("王座戦", iteration_str, "一次予選", group_str)
            if len(match_db_1_i) == 0:
                continue
            round_db_1_i = gen_round_name.read_round("王座戦", iteration_str, "一次予選", group_str)
            feed_1_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_1_i,
                                                                       "一次予選" + group_str,
                                                                       round_db_1_i),
                                            f"==={group_str}===\n",
                                            "王座戦",
                                            iteration_str,
                                            True,
                                            True,
                                            "◎",
                                            "")
            feed_1.append(feed_1_i)
            tree_1.append(feed_1_i.tree)
    elif iteration_int >= 4:
        for i in range(1):
            match_db_1_i = sql_read.read_match("王座戦", iteration_str, "一次予選")
            if len(match_db_1_i) == 0:
                continue
            round_db_1_i = gen_round_name.read_round("王座戦", iteration_str, "一次予選")
            feed_1_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_1_i,
                                                                       "一次予選",
                                                                       round_db_1_i),
                                            f"",
                                            "王座戦",
                                            iteration_str,
                                            True,
                                            True,
                                            "◎",
                                            "")
            feed_1.append(feed_1_i)
            tree_1.append(feed_1_i.tree)

    seeds_out_in.Seed(1, tree_1, tree_2, katakana_list)
    seeds_out_in.Seed(1, tree_2, tree_0, letter_list)
    if iteration_int >= 18:
        promoted_to_group_dict = dict()
        for tree in tree_0:
            for node in tree.last_remain_nodes:
                promoted_to_group_dict[node.winner().id] = "挑戦者"
        seeds_out_in.Seed(5, tree_0, [], [], [], promoted_to_group_dict)

    return_dict[0] = table_feed.draw_table_from_feed(feed_0)
    return_dict[2] = table_feed.draw_table_from_feed(feed_2)
    if len(feed_1) > 0:
        return_dict[1] = table_feed.draw_table_from_feed(feed_1)

    min_match_date = sql_read.read_match_min_max_date("王座戦", iteration_str, "MIN")[0]
    max_match_date = sql_read.read_match_min_max_date("王座戦", iteration_str, "MAX")[0]

    return_dict["INFOBOX"] = (
            "{{Infobox 各年の棋戦\n"
            + f"|期={iteration_str_display}\n"
            + "|イベント名称=王座戦\n"
            + f"|開催期間={min_match_date.isoformat()} - {max_match_date.isoformat()}\n"
            + "|タイトル=王座\n"
            + (f"|前タイトル={former_title.get_full_wiki_name()[0]}\n"
               if not new_title_flag
               else "")
            + f"|今期={iteration_str_display}\n"
            + f"|新タイトル={new_title.get_full_wiki_name()[0] if iteration_int >= 18 else winner_name[0]}\n"
            + "|△昇級△=\n"
            + "|▼降級▼=\n"
            + f"|前回=[[{iteration_str_prev}王座戦 (将棋)|{iteration_str_prev}]]\n"
            + f"|次回=[[{iteration_str_next}王座戦 (将棋)|{iteration_str_next}]]\n"
            + "}}\n"
    )

    return_dict["LEAD"] = (
        f"{iteration_str_display}王座戦は、{1952 + iteration_int}年度（{min_match_date.isoformat()}"
        f" - {max_match_date.isoformat()}）の[[王座戦 (将棋)|王座戦]]である。\n"
        + ("王座戦は将棋のタイトル戦の一つである。\n" if iteration_int >= 31 else "")
    )

    return return_dict
