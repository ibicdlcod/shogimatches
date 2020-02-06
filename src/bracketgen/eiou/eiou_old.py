from bracketgen import gen_round_name, str_list, title_match
from importdata import sql_read
from metastruct import organized_tr, seeds_out_in, table_feed


def eiou_str_dict(iteration_int: int) -> dict:
    return_dict = dict()

    iteration_str = f"第{str(iteration_int).zfill(2)}回"

    feed_0 = []
    tree_0 = []
    for i in range(1):
        match_db_0_i = sql_read.read_match("叡王戦", iteration_str, "本戦")
        round_db_0_i = gen_round_name.read_round("叡王戦", iteration_str, "本戦")
        feed_0_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_0_i,
                                                                   "本戦",
                                                                   round_db_0_i),
                                        f"",
                                        "叡王戦",
                                        iteration_str,
                                        True,
                                        False,
                                        "◎",
                                        "")
        feed_0.append(feed_0_i)
        tree_0.append(feed_0_i.tree)

    letter_group_list = ["Aブロック", "Bブロック", "Cブロック",
                         "Dブロック", "Eブロック", "Fブロック"]

    feed_9 = []
    tree_9 = []
    for i in range(6):
        group_str = letter_group_list[i]
        match_db_9_i = sql_read.read_match("叡王戦", iteration_str, "九段戦", group_str)
        if len(match_db_9_i) == 0:
            continue
        round_db_9_i = gen_round_name.read_round("叡王戦", iteration_str, "九段戦", group_str)
        feed_9_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_9_i,
                                                                   "九段戦" + group_str,
                                                                   round_db_9_i),
                                        f"==={group_str}===\n",
                                        "叡王戦",
                                        iteration_str,
                                        True,
                                        True,
                                        "◎",
                                        "")
        feed_9.append(feed_9_i)
        tree_9.append(feed_9_i.tree)

    feed_8 = []
    tree_8 = []
    for i in range(6):
        group_str = letter_group_list[i]
        match_db_8_i = sql_read.read_match("叡王戦", iteration_str, "八段戦", group_str)
        if len(match_db_8_i) == 0:
            continue
        round_db_8_i = gen_round_name.read_round("叡王戦", iteration_str, "八段戦", group_str)
        feed_8_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_8_i,
                                                                   "八段戦" + group_str,
                                                                   round_db_8_i),
                                        f"==={group_str}===\n",
                                        "叡王戦",
                                        iteration_str,
                                        True,
                                        True,
                                        "◎",
                                        "")
        feed_8.append(feed_8_i)
        tree_8.append(feed_8_i.tree)

    feed_7 = []
    tree_7 = []
    for i in range(6):
        group_str = letter_group_list[i]
        match_db_7_i = sql_read.read_match("叡王戦", iteration_str, "七段戦", group_str)
        if len(match_db_7_i) == 0:
            continue
        round_db_7_i = gen_round_name.read_round("叡王戦", iteration_str, "七段戦", group_str)
        feed_7_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_7_i,
                                                                   "七段戦" + group_str,
                                                                   round_db_7_i),
                                        f"==={group_str}===\n",
                                        "叡王戦",
                                        iteration_str,
                                        True,
                                        True,
                                        "◎",
                                        "")
        feed_7.append(feed_7_i)
        tree_7.append(feed_7_i.tree)

    feed_6 = []
    tree_6 = []
    for i in range(6):
        group_str = letter_group_list[i]
        match_db_6_i = sql_read.read_match("叡王戦", iteration_str, "六段戦", group_str)
        if len(match_db_6_i) == 0:
            continue
        round_db_6_i = gen_round_name.read_round("叡王戦", iteration_str, "六段戦", group_str)
        feed_6_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_6_i,
                                                                   "六段戦" + group_str,
                                                                   round_db_6_i),
                                        f"==={group_str}===\n",
                                        "叡王戦",
                                        iteration_str,
                                        True,
                                        True,
                                        "◎",
                                        "")
        feed_6.append(feed_6_i)
        tree_6.append(feed_6_i.tree)

    feed_5 = []
    tree_5 = []
    for i in range(6):
        group_str = letter_group_list[i]
        match_db_5_i = sql_read.read_match("叡王戦", iteration_str, "五段戦", group_str)
        if len(match_db_5_i) == 0:
            continue
        round_db_5_i = gen_round_name.read_round("叡王戦", iteration_str, "五段戦", group_str)
        feed_5_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_5_i,
                                                                   "五段戦" + group_str,
                                                                   round_db_5_i),
                                        f"==={group_str}===\n",
                                        "叡王戦",
                                        iteration_str,
                                        True,
                                        True,
                                        "◎",
                                        "")
        feed_5.append(feed_5_i)
        tree_5.append(feed_5_i.tree)

    feed_4 = []
    tree_4 = []
    for i in range(1):
        match_db_4_i = sql_read.read_match("叡王戦", iteration_str, "四段戦", )
        if len(match_db_4_i) == 0:
            continue
        round_db_4_i = gen_round_name.read_round("叡王戦", iteration_str, "四段戦")
        feed_4_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_4_i,
                                                                   "四段戦",
                                                                   round_db_4_i),
                                        f"",
                                        "叡王戦",
                                        iteration_str,
                                        True,
                                        True,
                                        "◎",
                                        "")
        feed_4.append(feed_4_i)
        tree_4.append(feed_4_i.tree)

    seeds_out_in.Seed(1, tree_9, tree_0, ["9A", "9B", "9C", "9D", "9E", "9F"])
    seeds_out_in.Seed(1, tree_8, tree_0, ["8A", "8B", "8C", "8D"])
    seeds_out_in.Seed(1, tree_7, tree_0, ["7A", "7B", "7C"])
    seeds_out_in.Seed(1, tree_6, tree_0, ["6A", "6B", "6C"])
    seeds_out_in.Seed(1, tree_5, tree_0, ["5A", "5B"])
    seeds_out_in.Seed(1, tree_4, tree_0, ["4"])

    winner_dict = dict()
    winner_name = ""
    for tree in tree_0:
        for node in tree.last_remain_nodes:
            winner_dict[node.winner().id] = "優勝"
            winner_name = node.winner().get_full_wiki_name()
    seeds_out_in.Seed(5, tree_0, [], [], [], winner_dict)

    return_dict[0] = table_feed.draw_table_from_feed(feed_0)
    return_dict[9] = table_feed.draw_table_from_feed(feed_9)
    return_dict[8] = table_feed.draw_table_from_feed(feed_8)
    return_dict[7] = table_feed.draw_table_from_feed(feed_7)
    return_dict[6] = table_feed.draw_table_from_feed(feed_6)
    return_dict[5] = table_feed.draw_table_from_feed(feed_5)
    return_dict[4] = table_feed.draw_table_from_feed(feed_4)

    min_match_date = sql_read.read_match_min_max_date("叡王戦", iteration_str, "MIN")[0]
    max_match_date = sql_read.read_match_min_max_date("叡王戦", iteration_str, "MAX")[0]

    return_dict["INFOBOX"] = (
            "{{Infobox 各年の棋戦\n"
            + f"|期=第{iteration_int}回\n"
            + "|イベント名称=叡王戦\n"
            + f"|開催期間={min_match_date.isoformat()} - {max_match_date.isoformat()}\n"
            + "|タイトル=叡王\n"
            + f"|今期=第{iteration_int}回\n"
            + f"|新タイトル={winner_name[0]}\n"
            + "|△昇級△=\n"
            + "|▼降級▼=\n"
            + (f"|前回=[[第{iteration_int - 1}回叡王戦|第{iteration_int - 1}回]]\n"
               if iteration_int != 1
               else "|前回=")
            + (f"|次回=[[第{iteration_int + 1}回叡王戦|第{iteration_int + 1}回]]\n"
               if iteration_int != 2
               else "|次回=[[第3期叡王戦|第3期]]")
            + "}}\n"
    )

    return_dict["LEAD"] = (
        f"第{iteration_int}期叡王戦は、{2014 + iteration_int}年度（{min_match_date.isoformat()}"
        f" - {max_match_date.isoformat()}）の[[叡王戦]]である。\n"
    )

    return return_dict
