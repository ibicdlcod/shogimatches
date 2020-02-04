from bracketgen import gen_round_name
from bracketgen.shidan import shidan_title_7
from importdata import sql_read
from metastruct import organized_tr, seeds_out_in, table_feed


def shidan_str_dict(iteration_int: int) -> dict:
    return_dict = dict()

    iteration_str = f"第{str(iteration_int).zfill(2)}期"

    return_dict[7] = shidan_title_7.shidan_title_matches(iteration_int)

    match_db_1 = sql_read.read_match("十段戦", iteration_str, "予選")
    round_db_1 = gen_round_name.read_round("十段戦", iteration_str, "予選")
    feed_1 = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_1,
                                                             "予選",
                                                             round_db_1),
                                  "==予選==\n",
                                  "十段戦",
                                  iteration_str,
                                  True,
                                  True,
                                  "◎",
                                  "")

    promoted_to_group_dict = dict()
    for node in feed_1.tree.last_remain_nodes:
        promoted_to_group_dict[node.winner().id] = "リーグ入り"
    seeds_out_in.Seed(5, [feed_1.tree, ], [], [], [], promoted_to_group_dict)

    return_dict[1] = table_feed.draw_table_from_feed([feed_1, ])

    return return_dict
