from metastruct import organized_t, tree_node, kishi_data, match_data
from metastruct import table_desc


def vertical_position(in_node: tree_node.TreeNode) -> list:
    return_val = []
    if in_node.black_q_from is None:
        return_val.append(in_node.black_of_first.id)
    else:
        for i in vertical_position(in_node.black_q_from):
            return_val.append(i)
    if in_node.white_q_from is None:
        return_val.append(in_node.white_of_first.id)
    else:
        for i in vertical_position(in_node.white_q_from):
            return_val.append(i)
    return return_val


def generate_bra_pos(in_tree: organized_t.OrganizedTree,
                     out_seed: dict,
                     in_seed: dict,
                     out_seed_disabled: bool = False,
                     in_seed_disabled: bool = False,
                     ):
    a = len(in_tree.list_round_num)
    seeds_in = in_seed
    seeds_in = {
        184: "4組優勝",
        102: "3組2位",
        115: "1組優勝",
        100: "1組3位",
        150: "2組2位",
        119: "2組優勝",
        42: "1組3位",
        170: "1組2位",
        198: "3組優勝",
        190: "5組優勝",
        201: "6組優勝",
    }
    seeds_out = {
        198: "挑戦者"
    }
    vertical_pos = []
    for nodes in in_tree.last_remain_nodes:
        for i in vertical_position(nodes):
            vertical_pos.append(i)
    position_dicts = []
    for i in range(a):
        position_dicts.append(dict())
    for i in range(len(vertical_pos)):
        position_dicts[a-1][vertical_pos[i]] = 2+2*i
    tree_into_layers = organized_t.nodes_layer_from_tr(in_tree)
    for i in tree_into_layers:
        for j in i:
            print(j)
        print()
    for i in range(a-1, -1, -1):
        prev_position = position_dicts[i]
        next_position = prev_position.copy()
        for j in tree_into_layers[i]:
            j_upper = j.black_of_first.id
            j_lower = j.white_of_first.id
            j_winner = None
            if j.advance_result == 0:
                print("Error: a match in a tree should have a winner")
                exit(3)
            elif j.advance_result > 0:
                j_winner = j_upper
            elif j.advance_result < 0:
                j_winner = j_lower
            next_position.pop(j_upper)
            next_position.pop(j_lower)
            next_position[j_winner] = (prev_position[j_upper] + prev_position[j_lower]) // 2
        if i != 0:
            position_dicts[i-1] = next_position
    table_pos_all = []
    # upper
    row_num = 0
    factor = 4 if out_seed_disabled else 5
    for col_num_pri in range(a-1, -1, -1):
        u = 0
        if out_seed_disabled and col_num_pri != 0:
            u = 2
        else:
            u = 3
        t = table_desc.TableDesc(
            (row_num, factor * (a - col_num_pri - 1) + 1),
            (row_num, factor * (a - col_num_pri - 1) + u),
            in_tree.list_round_num[col_num_pri],
            "#dedede",
            False,
            (True, True, True, True)
        )
        table_pos_all.append(t)
    # kishi names
    have_match_dicts = []
    for i in range(a):
        have_match_dicts.append(dict())
    new_match_dicts = []
    for i in range(a):
        new_match_dicts.append(dict())
    for j in range(a):
        for k in position_dicts[j].keys():
            if j != a-1 and position_dicts[j][k] != position_dicts[j+1][k]:
                have_match_dicts[j][k] = True
            if j != 0 and k not in position_dicts[j-1].keys():
                have_match_dicts[j][k] = True
            if j != 0 and k in position_dicts[j-1].keys() and position_dicts[j][k] != position_dicts[j-1][k]:
                have_match_dicts[j][k] = True
    for j in range(a):
        for k in have_match_dicts[j].keys():
            if j == a-1:
                new_match_dicts[j][k] = True
            elif k not in have_match_dicts[j+1].keys():
                new_match_dicts[j][k] = True
    kishi_surname_table = []
    for k in vertical_pos:
        this_kishi = kishi_data.query_kishi_from_id(k)
        this_kishi_surname = this_kishi.fullname[:this_kishi.surname_length]
        kishi_surname_table.append(this_kishi_surname)
    for j in range(a):
        for k in have_match_dicts[j].keys():
            this_kishi = kishi_data.query_kishi_from_id(k)
            this_node, black_or_white = match_data.query_node_from_id(tree_into_layers[j], k)
            if k in new_match_dicts[j].keys() and (not in_seed_disabled):
                t1 = table_desc.TableDesc(
                    (position_dicts[j][k], factor * (a - j - 1)),
                    (position_dicts[j][k]+1, factor * (a - j - 1)),
                    seeds_in[k] if k in seeds_in.keys() else "",
                    "#f9f9f9",
                )
                table_pos_all.append(t1)
            if k in new_match_dicts[j].keys() or j == 0:
                if this_kishi.wiki_name == "":
                    kishi_display_name = "[[" \
                                        + this_kishi.fullname\
                                        + "]]" \
                                        + this_kishi.rank(this_node.series[0].match_date)
                else:
                    kishi_display_name = "[[" \
                                         + this_kishi.wiki_name \
                                         + "|" \
                                         + this_kishi.fullname \
                                         + "]]" \
                                         + this_kishi.rank(this_node.series[0].match_date)
            elif kishi_surname_table.count(this_kishi.fullname[:this_kishi.surname_length]) > 1:
                kishi_display_name = this_kishi.fullname[:this_kishi.surname_length+1]
            else:
                kishi_display_name = this_kishi.fullname[:this_kishi.surname_length]
            t2 = table_desc.TableDesc(
                (position_dicts[j][k], factor * (a - j - 1) + 1),
                (position_dicts[j][k]+1, factor * (a - j - 1) + 1),
                kishi_display_name,
                "#f9f9f9",
            )
            table_pos_all.append(t2)
            match_icons = ""
            for match in this_node.series:
                if len(this_node.series) > 1:
                    if match.black_name == kishi_data.query_kishi_from_id(k).fullname:
                        black_or_white = "black"
                    elif match.white_name == kishi_data.query_kishi_from_id(k).fullname:
                        black_or_white = "white"
                match_icon = ""
                match_icon += ("千" * match.sennichite)
                match_icon += ("持" * match.mochishogi)
                if match.sennichite == 0 and match.mochishogi == 0 and match.win_loss_for_black == 0:
                    match_icon = "無"
                elif match.forfeit_active:
                    if black_or_white == "black" and match.win_loss_for_black > 0:
                        match_icon += "□"
                    elif black_or_white == "white" and match.win_loss_for_black < 0:
                        match_icon += "□"
                    else:
                        match_icon += "■"
                else:
                    if black_or_white == "black" and match.win_loss_for_black > 0:
                        match_icon += "○"
                    elif black_or_white == "white" and match.win_loss_for_black < 0:
                        match_icon += "○"
                    elif black_or_white == "black" and match.win_loss_for_black < 0:
                        match_icon += "●"
                    elif black_or_white == "white" and match.win_loss_for_black > 0:
                        match_icon += "●"
                match_icons += match_icon
            t3 = table_desc.TableDesc(
                (position_dicts[j][k], factor * (a - j - 1) + 2),
                (position_dicts[j][k]+1, factor * (a - j - 1) + 2),
                match_icons,
                "#f9f9f9",
            )
            table_pos_all.append(t3)
            out_seed_text = seeds_out[k] if k in seeds_out.keys() else ""
            if j != 0 and k in have_match_dicts[j-1].keys():
                out_seed_text = ""
            if j == 0 or (not out_seed_disabled):
                t4 = table_desc.TableDesc(
                    (position_dicts[j][k], factor * (a - j - 1) + 3),
                    (position_dicts[j][k] + 1, factor * (a - j - 1) + 3),
                    out_seed_text,
                    "#f9f9f9",
                )
                table_pos_all.append(t4)

    for t in table_pos_all:
        print(t)
