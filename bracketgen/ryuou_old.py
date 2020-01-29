from metastruct import organized_t, seeds_out_in
from bracketgen import bra_from_tr
from importdata import sql_read, gen_round_name


def ryuou_old_str(iteration: str) -> str:
    return_result = ""
    letter_list = []
    for i in range(64, 90):
        letter_list.append(chr(i + 1))
    for i in range(96, 122):
        letter_list.append(chr(i + 1))

    # 決勝トーナメント
    return_result += "==決勝トーナメント==\n"
    match_db0 = sql_read.read_match("竜王戦", iteration, "決勝トーナメント")
    round_db0 = gen_round_name.read_round("竜王戦", iteration, "決勝トーナメント")
    org_tree0 = organized_t.OrganizedTree(match_db0, "決勝トーナメント", round_db0)
    table_0 = bra_from_tr.generate_bra_pos(org_tree0, dict(), dict(), True, True)
    draw_table_0 = bra_from_tr.draw_table(table_0, "竜王戦" + iteration + org_tree0.display_name)
    return_result += draw_table_0

    org_tree1_a = get_x_group_normal_tree(iteration, 1)
    org_tree1_b = get_1_group_appear_round_tree(iteration, 3)

    # match_db3 = sql_read.read_match("竜王戦", iteration, "1組", "3位出場者決定戦")
    # round_db3 = gen_round_name.read_round("竜王戦", iteration, "1組", "3位出場者決定戦")
    # print(round_db3)
    # org_tree3 = organized_t.OrganizedTree(match_db3, "1組3位出場者決定戦", round_db3)

    s = seeds_out_in.Seed(-2, [org_tree1_a, ], [org_tree1_b, ], letter_list)
    s.assign_seed()

    # return_result += "==1組==\n"
    # return_result += "===ランキング戦===\n"
    # table_2 = bra_from_tr.generate_bra_pos(org_tree1_a, dict(), dict(), False, True)
    # draw_table_2 = bra_from_tr.draw_table(table_2, "竜王戦" + iteration + org_tree1_a.display_name)
    # return_result += draw_table_2
    # return_result += "===3位出場者決定戦===\n"
    # table_3 = bra_from_tr.generate_bra_pos(org_tree1_b, dict(), dict(), False, False)
    # draw_table_3 = bra_from_tr.draw_table(table_3, "竜王戦" + iteration + org_tree1_b.display_name)
    # return_result += draw_table_3

    in_trees = [org_tree1_a, org_tree1_b]
    prefixes = ["==1組==\n===ランキング戦===\n",
                "===3位出場者決定戦===\n"]
    out_seed_disable_s = [False, False]
    in_seed_disable_s = [True, False]
    first_place_labels_s = ["◎", "◎"]
    second_place_labels_s = ["◎", ""]
    for i in range(2, 7):
        tree_normal = get_x_group_normal_tree(iteration, i)
        in_trees.append(tree_normal)
        prefixes.append(f"=={i}組==\n===ランキング戦===\n")
        out_seed_disable_s.append(False)
        in_seed_disable_s.append(True)
        first_place_labels_s.append("◎")
        second_place_labels_s.append("◎" if i < 4 else "△")
        tree_promo = get_x_group_promo_round_tree(iteration, i)
        in_trees.append(tree_promo)
        prefixes.append(f"===昇級者決定戦===\n")
        out_seed_disable_s.append(True if i == 6 else False)
        in_seed_disable_s.append(False)
        first_place_labels_s.append("△")
        second_place_labels_s.append("")
        s = seeds_out_in.Seed(-2, [tree_normal, ], [tree_promo, ], letter_list)
        s.assign_seed()
    return_result += draw_table_from_trees(in_trees, prefixes, "竜王戦", iteration,
                                           out_seed_disable_s,
                                           in_seed_disable_s,
                                           first_place_labels_s,
                                           second_place_labels_s)

    return return_result


def get_x_group_normal_tree(iteration:str, group_num: int):
    match_db = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "ランキング戦")
    round_db = gen_round_name.read_round("竜王戦", iteration, f"{group_num}組", "ランキング戦")
    org_tree = organized_t.OrganizedTree(match_db, f"{group_num}組ランキング戦", round_db)
    return org_tree


def get_x_group_promo_round_tree(iteration:str, group_num: int):
    match_db = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "昇級者決定戦")
    round_db = gen_round_name.read_round("竜王戦", iteration, f"{group_num}組", "昇級者決定戦")
    org_tree = organized_t.OrganizedTree(match_db, f"{group_num}組昇級者決定戦", round_db)
    return org_tree


def get_1_group_appear_round_tree(iteration:str, pos_num: int):
    match_db = sql_read.read_match("竜王戦", iteration, "1組", f"{pos_num}位出場者決定戦")
    round_db = gen_round_name.read_round("竜王戦", iteration, "1組", f"{pos_num}位出場者決定戦")
    org_tree = organized_t.OrganizedTree(match_db, f"1組{pos_num}位出場者決定戦", round_db)
    return org_tree


def draw_table_from_trees(in_trees, prefixes, tournament_name: str,
                          iteration: str,
                          out_seed_disable_s,
                          in_seed_disable_s,
                          first_place_labels_s,
                          second_place_labels_s) -> str:
    result = ""
    for i in range(len(in_trees)):
        result += prefixes[i]
        in_tree = in_trees[i]
        table = bra_from_tr.generate_bra_pos(in_tree, dict(), dict(),
                                             out_seed_disable_s[i],
                                             in_seed_disable_s[i],
                                             first_place_labels_s[i],
                                             second_place_labels_s[i])
        draw_table = bra_from_tr.draw_table(table, tournament_name + iteration + in_tree.display_name)
        result += draw_table
    return result
