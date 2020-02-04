from bracketgen import gen_round_name, title_match, str_list
from bracketgen.shidan import shidan_title_7
from importdata import sql_read
from metastruct import organized_tr, seeds_out_in, table_feed


def shidan_str_dict(iteration_int: int) -> dict:
    return_dict = dict()
    katakana_list = str_list.katakana_list
    hiragana_list = str_list.hiragana_list

    iteration_str = f"第{str(iteration_int).zfill(2)}期"

    return_dict[7] = shidan_title_7.shidan_title_matches(iteration_int)

    feed_3 = []
    tree_3 = []
    for i in range(2):
        group_str = f"{str(i + 1).zfill(2)}組"
        match_db_3_i = sql_read.read_match("十段戦", iteration_str, "三次予選", group_str)
        round_db_3_i = gen_round_name.read_round("十段戦", iteration_str, "三次予選", group_str)
        feed_3_i = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_3_i,
                                                                   "三次予選" + group_str,
                                                                   round_db_3_i),
                                        f"==={group_str}===\n",
                                        "十段戦",
                                        iteration_str,
                                        True,
                                        False,
                                        "◎",
                                        "")
        feed_3.append(feed_3_i)
        tree_3.append(feed_3_i.tree)

    feed_2 = []
    tree_2 = []
    for i in range(8):
        if i == 6:
            a = 1

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
    seeds_out_in.Seed(1, tree_2, tree_3, katakana_list)
    promoted_to_group_dict = dict()
    for tree in tree_3:
        for node in tree.last_remain_nodes:
            promoted_to_group_dict[node.winner().id] = "リーグ入り&nbsp;"
    seeds_out_in.Seed(5, tree_3, [], [], [], promoted_to_group_dict)

    return_dict[3] = table_feed.draw_table_from_feed(feed_3)
    return_dict[2] = table_feed.draw_table_from_feed(feed_2)
    return_dict[1] = table_feed.draw_table_from_feed(feed_1)

    return return_dict
