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
                     first_place_label: str = "",
                     second_place_label: str = "",
                     ) -> list:
    # split tree
    if len(in_tree.last_remain_nodes) > 1:
        s = 0
        for last_node in in_tree.last_remain_nodes:
            s += 1
            this_part_nodes = [last_node, ]
            for i in range(1, len(in_tree.list_round_num)):
                for node in this_part_nodes:
                    if node.black_q_from in in_tree.node_groups[i]:
                        this_part_nodes.append(node.black_q_from)
                    if node.white_q_from in in_tree.node_groups[i]:
                        this_part_nodes.append(node.white_q_from)
            this_part_matches = []
            for j in this_part_nodes:
                for k in j.series:
                    this_part_matches.append(k)
            sub_org_tree = organized_t.OrganizedTree(this_part_matches, in_tree.list_round_prefix,
                                      in_tree.list_round_num, in_tree.list_round_prefix + f"({s})")
            generate_bra_pos(sub_org_tree,
                             out_seed,
                             in_seed,
                             out_seed_disabled,
                             in_seed_disabled,
                             first_place_label,
                             second_place_label)
            print(this_part_nodes)
            print()

    a = len(in_tree.list_round_num)
    first_place_label = "◎"
    second_place_label = "△"

    in_seed = {
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
    out_seed = {
        198: "挑戦者",
        184: "4組優勝",
        102: "3組2位",
        115: "1組優勝",
        100: "1組3位",
        150: "2組2位",
        119: "2組優勝",
        42: "1組3位",
        170: "1組2位",
        190: "5組優勝",
        201: "6組優勝",
    }
    vertical_pos = []
    for nodes in in_tree.last_remain_nodes:
        for i in vertical_position(nodes):
            vertical_pos.append(i)
    position_dicts = []
    for i in range(a):
        position_dicts.append(dict())
    for i in range(len(vertical_pos)):
        position_dicts[a - 1][vertical_pos[i]] = 2 + 2 * i
    tree_into_layers = organized_t.nodes_layer_from_tr(in_tree)
    for i in range(a - 1, -1, -1):
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
            position_dicts[i - 1] = next_position
    table_pos_all = []
    # upper
    row_num = 0
    factor = 4 if out_seed_disabled else 5
    for col_num_pri in range(a - 1, -1, -1):
        u = 0
        if out_seed_disabled and col_num_pri != 0:
            u = 2
        else:
            u = 3
        t = table_desc.TableDesc(
            (row_num, factor * (a - col_num_pri - 1) + 2),
            (row_num, factor * (a - col_num_pri - 1) + u + 2),
            False,
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
            if j == 0:
                have_match_dicts[j][k] = True
            if j != a - 1 and position_dicts[j][k] != position_dicts[j + 1][k]:
                have_match_dicts[j][k] = True
            if j != 0 and k not in position_dicts[j - 1].keys():
                have_match_dicts[j][k] = True
            if j != 0 and k in position_dicts[j - 1].keys() and position_dicts[j][k] != position_dicts[j - 1][k]:
                have_match_dicts[j][k] = True
    for j in range(a):
        for k in have_match_dicts[j].keys():
            if j == a - 1:
                new_match_dicts[j][k] = True
            elif k not in have_match_dicts[j + 1].keys():
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
            new_flag = False
            if k in new_match_dicts[j].keys() and (not in_seed_disabled):
                column_from_1 = (factor * (a - j - 1) - (0 if j == a - 1 else 3)
                                 + (2 if not out_seed_disabled else 2))
                column_to_1 = factor * (a - j - 1) + 1
                if column_from_1 > column_to_1:
                    column_from_1 = column_to_1
                t1 = table_desc.TableDesc(
                    (position_dicts[j][k], column_from_1),
                    (position_dicts[j][k] + 1, column_to_1),
                    False,
                    in_seed[k] if k in in_seed.keys() else "",
                    "#f9f9f9",
                )
                table_pos_all.append(t1)
            if k in new_match_dicts[j].keys():
                new_flag = True
            if k in new_match_dicts[j].keys() or j == 0:
                if this_kishi.wiki_name == "":
                    rank = this_kishi.rank(this_node.series[0].match_date)[0]
                    kishi_display_name = "[[" \
                                         + this_kishi.fullname \
                                         + "]]" \
                                         + rank
                else:
                    kishi_display_name = "[[" \
                                         + this_kishi.wiki_name \
                                         + "|" \
                                         + this_kishi.fullname \
                                         + "]]" \
                                         + this_kishi.rank(this_node.series[0].match_date)[0]
            elif kishi_surname_table.count(this_kishi.fullname[:this_kishi.surname_length]) > 1:
                kishi_display_name = this_kishi.fullname[:this_kishi.surname_length + 1]
            else:
                kishi_display_name = this_kishi.fullname[:this_kishi.surname_length]

            if k in new_match_dicts[j].keys() or j == 0:
                kishi_display_name_len = len(this_kishi.fullname) * 1.4 \
                                         + this_kishi.rank(this_node.series[0].match_date)[1]
            elif kishi_surname_table.count(this_kishi.fullname[:this_kishi.surname_length]) > 1:
                kishi_display_name_len = len(this_kishi.fullname[:this_kishi.surname_length + 1]) * 1.4
            else:
                kishi_display_name_len = len(this_kishi.fullname[:this_kishi.surname_length]) * 1.4

            last_winners = [node.winner() for node in in_tree.last_remain_nodes]
            if this_kishi in last_winners and first_place_label != "":
                kishi_display_name = "'''" + kishi_display_name \
                                     + "'''" + (first_place_label if new_flag else "")
            last_losers = [node.loser() for node in in_tree.last_remain_nodes]
            if this_kishi in last_losers and second_place_label != "":
                kishi_display_name = ("'''" if j != 0 else "") + kishi_display_name \
                                     + ("'''" if j != 0 else "") + (second_place_label if new_flag else "")
            t2 = table_desc.TableDesc(
                (position_dicts[j][k], factor * (a - j - 1) + 2),
                (position_dicts[j][k] + 1, factor * (a - j - 1) + 2),
                False,
                kishi_display_name,
                "#f9f9f9",
                False,
                (True, True, True, True),
                kishi_display_name_len
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
                (position_dicts[j][k], factor * (a - j - 1) + 3),
                (position_dicts[j][k] + 1, factor * (a - j - 1) + 3),
                False,
                match_icons,
                "#f9f9f9",
            )
            table_pos_all.append(t3)
            out_seed_text = out_seed[k] if k in out_seed.keys() else ""
            if j != 0 and k in have_match_dicts[j - 1].keys():
                out_seed_text = ""
            if j == 0 or (not out_seed_disabled):
                t4 = table_desc.TableDesc(
                    (position_dicts[j][k], factor * (a - j - 1) + 4),
                    (position_dicts[j][k] + 1, factor * (a - j - 1) + 4),
                    False,
                    out_seed_text,
                    "#f9f9f9",
                )
                table_pos_all.append(t4)
    # black lines
    for j in range(a):
        for node in tree_into_layers[j]:
            pos1 = position_dicts[j][node.black_of_first.id] + 1
            pos2 = position_dicts[j][node.white_of_first.id]
            t5 = table_desc.TableDesc(
                (pos1, factor * (a - j) - (0 if (factor == 4 and j == 0) else 1) + 1),
                (pos2, factor * (a - j) - (0 if (factor == 4 and j == 0) else 1) + 1),
                False,
                "",
                "#FFFFFF",
                True,
                (True, True, True, False)
            )
            table_pos_all.append(t5)
            pos3 = (pos1 + pos2 - 1) // 2
            if j != 0:
                t6 = table_desc.TableDesc(
                    (pos3, factor * (a - j) - (0 if (factor == 4 and j == 0) else 1) + 2),
                    (pos3, factor * (a - j) - (0 if (factor == 4 and j == 0) else 1) + 2),
                    False,
                    "",
                    "#FFFFFF",
                    True,
                    (False, False, True, False)
                )
                table_pos_all.append(t6)
    occupied_grid = []
    row_limit = max([cell.to_cell[0] for cell in table_pos_all]) + 1
    column_limit = max([cell.to_cell[1] for cell in table_pos_all]) + 1
    for i in range(row_limit):
        occupied_grid.append([])
        for j in range(column_limit):
            occupied_grid[i].append(False)
    for cell in table_pos_all:
        from_row = cell.from_cell[0]
        from_col = cell.from_cell[1]
        to_row = cell.to_cell[0] + 1
        to_col = cell.to_cell[1] + 1
        for i in range(from_row, to_row):
            for j in range(from_col, to_col):
                occupied_grid[i][j] = True
    for i in range(row_limit):
        j = 0
        while j < column_limit:
            if not occupied_grid[i][j]:
                k = j
                while k < column_limit - 1:
                    if occupied_grid[i][k + 1]:
                        break
                    k += 1
                t7 = table_desc.TableDesc(
                    (i, j),
                    (i, k),
                    True,
                )
                table_pos_all.append(t7)
                j = k + 1
            else:
                j += 1
    table_pos_all.sort(key=lambda cell: (cell.from_cell[0], cell.from_cell[1]))
    return table_pos_all


def draw_table(in_table_list: list) -> str:
    return_block = ""
    row_limit = max([cell.to_cell[0] for cell in in_table_list]) + 1
    column_limit = max([cell.to_cell[1] for cell in in_table_list]) + 1
    # for row 0
    return_block += '{| border="0" cellpadding="0" cellspacing="0" style="font-size: 70%;"\n'
    # column names
    return_block += '| &nbsp;\n'
    in_table_list_cur_index = 1
    while True:
        current_cell = in_table_list[in_table_list_cur_index]
        if current_cell.from_cell[0] > 0:
            break
        if not current_cell.empty:
            return_block += (f'| align="center" colspan="'
                             f'{current_cell.to_cell[1] - current_cell.from_cell[1] + 1}'
                             f'" style="border:1px solid #aaa;" bgcolor="'
                             f'{current_cell.bg_color}" |'
                             f'{current_cell.content}\n')
        else:
            return_block += (f'| colspan="'
                             f'{current_cell.to_cell[1] - current_cell.from_cell[1] + 1}'
                             f'" |\n'
                             )
        in_table_list_cur_index += 1
    # for row 1
    return_block += '|-\n|'
    # calculate column width
    column_width = []
    for j in range(column_limit):
        column_width.append(0.5)
    in_table_list.sort(key=lambda cell: cell.to_cell[1] - cell.from_cell[1])
    for cell in in_table_list:
        if cell.empty or cell.content == '':
            continue
        else:
            columns = range(cell.from_cell[1], cell.to_cell[1] + 1)
            content_length = cell.content_len
            if content_length != 0 and content_length < 3:
                content_length += 1
            if 3 <= content_length < 5:
                content_length += 0.5
            current_col_length = sum([column_width[column] for column in columns])
            while current_col_length < content_length:
                for column in columns:
                    column_width[column] += 0.5
                current_col_length = sum([column_width[column] for column in columns])
    in_table_list.sort(key=lambda cell: (cell.from_cell[0], cell.from_cell[1]))
    for i in range(column_limit):
        if i == 0:
            return_block += f'style="height:0.5em; width:{column_width[i]}em"| '
        else:
            return_block += f'||style="width:{column_width[i]}em"| '
    return_block += '\n'
    # for row 2 onwards
    for row_num in range(2, row_limit):
        flag = 0
        return_block += '|-\n'
        while True:
            current_cell = in_table_list[in_table_list_cur_index]
            if current_cell.from_cell[0] < row_num:
                in_table_list_cur_index += 1
            else:
                break
        while True:
            current_cell = in_table_list[in_table_list_cur_index]
            if current_cell.from_cell[0] > row_num:
                break
            if flag == 0:
                return_block += '|style="height:1em" '
                flag += 1
            else:
                return_block += f'||'
            rowspan_describe = (f'rowspan="'
                                f'{current_cell.to_cell[0] - current_cell.from_cell[0] + 1}'
                                f'" ')
            colspan_describe = (f'colspan="'
                                f'{current_cell.to_cell[1] - current_cell.from_cell[1] + 1}'
                                f'" ')
            if current_cell.to_cell[0] == current_cell.from_cell[0]:
                rowspan_describe = ''
            if current_cell.to_cell[1] == current_cell.from_cell[1]:
                colspan_describe = ''
            solid_border = f'style="border:1px solid #aaa;text-align:center" bgcolor="{current_cell.bg_color}"'
            up = "1px" if current_cell.border_up else 0
            right = "1px" if current_cell.border_right else 0
            down = "1px" if current_cell.border_down else 0
            left = "1px" if current_cell.border_left else 0
            black_border = f'style="border-width:{up} {right} {down} {left}; border-style:solid; border-color:black;"'
            if not current_cell.border_black:
                return_block += (rowspan_describe + colspan_describe
                                 + (solid_border if (not current_cell.empty) else '')
                                 + f' |'
                                 f'{current_cell.content}')
            else:
                return_block += (rowspan_describe + colspan_describe
                                 + black_border +
                                 f' |'
                                 f'{current_cell.content}')
            return_block += " "
            in_table_list_cur_index += 1
            if in_table_list_cur_index >= len(in_table_list):
                break
        return_block += "\n"

    return_block += "|}\n<br/>\n"
    return return_block
