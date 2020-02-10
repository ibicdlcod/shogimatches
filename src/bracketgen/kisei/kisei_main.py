from bracketgen import gen_round_name, str_list
from bracketgen.kisei import kisei_common
from importdata import sql_read
from metastruct import organized_tr, seeds_out_in, table_feed


def kisei_str_dict(iteration_int: int) -> dict:
    return_dict = dict()
    letter_list = str_list.letter_list
    katakana_list = str_list.katakana_list

    iteration_str = f"第{str(iteration_int).zfill(2)}期"
    iteration_str_display = f"第{str(iteration_int)}期"
    iteration_str_prev = (f"第{str(iteration_int - 1)}期"
                          if iteration_int >= 2
                          else f"")
    iteration_str_next = f"第{str(iteration_int + 1)}期"

    title_result = kisei_common.kisei_title_matches(iteration_int)
    return_dict["T"] = title_result[0]
    new_title_flag = title_result[1]
    former_title = title_result[2]
    new_title = title_result[3]

    feed_0 = []
    tree_0 = []
    if iteration_int >= 2:
        main_tournament_name = "本戦" if iteration_int < 66 else "決勝トーナメント"
        for i in range(1):
            match_db_0_i = sql_read.read_match("棋聖戦", iteration_str, main_tournament_name)
            round_db_0_i = gen_round_name.read_round("棋聖戦", iteration_str, main_tournament_name)
            feed_0_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_0_i,
                                                                       main_tournament_name,
                                                                       round_db_0_i),
                                            f"",
                                            "棋聖戦",
                                            iteration_str,
                                            True,
                                            False,
                                            "◎",
                                            "")
            feed_0.append(feed_0_i)
            tree_0.append(feed_0_i.tree)

        challenge_dict = dict()
        for tree in tree_0:
            for node in tree.last_remain_nodes:
                challenge_dict[node.winner().id] = "挑戦者"
        seeds_out_in.Seed(5, tree_0, [], [], [], challenge_dict)

    feed_2 = []
    tree_2 = []
    if 2 <= iteration_int <= 27 or iteration_int >= 85:
        for i in range(12):
            group_str = f"{str(i + 1).zfill(2)}組"
            match_db_2_i = sql_read.read_match("棋聖戦", iteration_str, "二次予選", group_str)
            if len(match_db_2_i) == 0:
                continue
            round_db_2_i = gen_round_name.read_round("棋聖戦", iteration_str, "二次予選", group_str)
            feed_2_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_2_i,
                                                                       "二次予選" + group_str,
                                                                       round_db_2_i),
                                            f"==={group_str}===\n",
                                            "棋聖戦",
                                            iteration_str,
                                            True,
                                            False,
                                            "◎",
                                            "")
            feed_2.append(feed_2_i)
            tree_2.append(feed_2_i.tree)
    elif iteration_int >= 2:
        for i in range(1):
            match_db_2_i = sql_read.read_match("棋聖戦", iteration_str, "二次予選")
            if len(match_db_2_i) == 0:
                continue
            round_db_2_i = gen_round_name.read_round("棋聖戦", iteration_str, "二次予選")
            feed_2_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_2_i,
                                                                       "二次予選",
                                                                       round_db_2_i),
                                            f"",
                                            "棋聖戦",
                                            iteration_str,
                                            True,
                                            False,
                                            "◎",
                                            "")
            feed_2.append(feed_2_i)
            tree_2.append(feed_2_i.tree)

    feed_1 = []
    tree_1 = []
    group_1_str_list = ["イ組", "ロ組", "ハ組", "ニ組", "ホ組", "ヘ組", "ト組", "チ組"]
    if 2 <= iteration_int <= 28 or iteration_int >= 85:
        for i in range(8):
            if 4 <= iteration_int <= 10 or iteration_int >= 85:
                group_str = group_1_str_list[i]
            else:
                group_str = f"{str(i + 1).zfill(2)}組"
            match_db_1_i = sql_read.read_match("棋聖戦", iteration_str, "一次予選", group_str)
            if len(match_db_1_i) == 0:
                continue
            round_db_1_i = gen_round_name.read_round("棋聖戦", iteration_str, "一次予選", group_str)
            feed_1_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_1_i,
                                                                       "一次予選" + group_str,
                                                                       round_db_1_i),
                                            f"==={group_str}===\n",
                                            "棋聖戦",
                                            iteration_str,
                                            True,
                                            True,
                                            "◎",
                                            "")
            feed_1.append(feed_1_i)
            tree_1.append(feed_1_i.tree)
    elif iteration_int >= 2:
        for i in range(1):
            match_db_1_i = sql_read.read_match("棋聖戦", iteration_str, "一次予選")
            if len(match_db_1_i) == 0:
                continue
            round_db_1_i = gen_round_name.read_round("棋聖戦", iteration_str, "一次予選")
            feed_1_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_1_i,
                                                                       "一次予選",
                                                                       round_db_1_i),
                                            f"",
                                            "棋聖戦",
                                            iteration_str,
                                            True,
                                            True,
                                            "◎",
                                            "")
            feed_1.append(feed_1_i)
            tree_1.append(feed_1_i.tree)

    seeds_out_in.Seed(1, tree_1, tree_2, katakana_list)
    if iteration_int < 66 or iteration_int > 80:
        seeds_out_in.Seed(1, tree_2, tree_0, letter_list)

    if len(feed_0) != 0:
        return_dict[0] = table_feed.draw_table_from_feed(feed_0)
    else:
        group_result = kisei_common.kisei_iter1_group(iteration_int)
        return_dict["TG"] = group_result
    return_dict[2] = table_feed.draw_table_from_feed(feed_2)
    return_dict[1] = table_feed.draw_table_from_feed(feed_1)

    min_match_date = sql_read.read_match_min_max_date("棋聖戦", iteration_str, "MIN")[0]
    max_match_date = sql_read.read_match_min_max_date("棋聖戦", iteration_str, "MAX")[0]

    return_dict["INFOBOX"] = (
            "{{Infobox 各年の棋戦\n"
            + f"|期={iteration_str_display}\n"
            + "|イベント名称=棋聖戦\n"
            + f"|開催期間={min_match_date.isoformat()} - {max_match_date.isoformat()}\n"
            + "|タイトル=棋聖\n"
            + (f"|前タイトル={former_title.get_full_wiki_name()[0]}\n"
               if not new_title_flag
               else "")
            + f"|今期={iteration_str_display}\n"
            + f"|新タイトル={new_title.get_full_wiki_name()[0]}\n"
            + "|△昇級△=\n"
            + "|▼降級▼=\n"
            + (f"|前回=[[{iteration_str_prev}棋聖戦|{iteration_str_prev}]]\n"
               if iteration_int >= 2
               else f"|前回=")
            + f"|次回=[[{iteration_str_next}棋聖戦|{iteration_str_next}]]\n"
            + "}}\n"
    )

    first_or_second_half = ""
    if iteration_int < 66:
        if (iteration_int % 2) == 0:
            first_or_second_half = "前期"
        else:
            first_or_second_half = "後期"
    if iteration_int < 66:
        year_held = (iteration_int // 2) + 1962
    else:
        year_held = 1929 + iteration_int

    return_dict["LEAD"] = (
        f"{iteration_str_display}棋聖戦は、{year_held}年度{first_or_second_half}（{min_match_date.isoformat()}"
        f" - {max_match_date.isoformat()}）の[[棋聖戦 (将棋)|棋聖戦]]である。\n"
        + "棋聖戦は将棋のタイトル戦の一つである。\n"
    )

    return return_dict
