from metastruct import kishi_data, match_data, organized_tab
from metastruct import organized_tr, table_desc, tree_node


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


def generate_bra_pos(in_tree: organized_tr.OrganizedTree,
                     in_seed: dict = None,
                     out_seed: dict = None,
                     out_seed_disabled: bool = False,
                     in_seed_disabled: bool = False,
                     first_place_label: str = "",
                     second_place_label: str = "",
                     ) -> organized_tab.OrganizedTable:
    if in_seed is not None:
        if len(in_seed.keys()) == 0 and in_tree.in_seed is not None:
            in_seed = in_tree.in_seed
    if out_seed is not None:
        if len(out_seed.keys()) == 0 and in_tree.out_seed is not None:
            out_seed = in_tree.out_seed
    # split tree
    if len(in_tree.last_remain_nodes) > 1 and in_tree.total_nodes > 18:
        sub_trees = organized_tr.split_with_multiple_winners(in_tree)
        sub_table_alt = []
        for tr in sub_trees:
            sub_table_alt.append(generate_bra_pos(tr,
                                                  in_seed,
                                                  out_seed,
                                                  out_seed_disabled,
                                                  in_seed_disabled,
                                                  first_place_label,
                                                  second_place_label))
        # return_result = table_desc.union_table(sub_table_alt)
        return_result = organized_tab.union_table_with_dict(sub_table_alt)
        return return_result

    a = len(in_tree.list_round_num)
    vertical_pos = []
    for nodes in in_tree.last_remain_nodes:
        for i in vertical_position(nodes):
            vertical_pos.append(i)
    position_dicts = []
    for i in range(a):
        position_dicts.append(dict())
    for i in range(len(vertical_pos)):
        position_dicts[a - 1][vertical_pos[i]] = 2 + 2 * i
    tree_into_layers = organized_tr.nodes_layer_from_tr(in_tree)
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
        if out_seed_disabled and col_num_pri != 0:
            u = 2
        else:
            u = 3
        t = table_desc.TableDesc(
            (row_num, factor * (a - col_num_pri - 1) + 2),
            (row_num, factor * (a - col_num_pri - 1) + u + 1),
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
    column_disabled_dict = dict()
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
                if k in in_seed.keys() and len(in_seed[k]) > 0:
                    t1 = table_desc.TableDesc(
                        (position_dicts[j][k], column_from_1),
                        (position_dicts[j][k] + 1, column_to_1),
                        False,
                        in_seed[k] if k in in_seed.keys() else "",
                        "#fff0f0" if this_kishi.woman else "#f9f9f9",
                    )
                    table_pos_all.append(t1)
                empty = (len(in_seed[k] if k in in_seed.keys() else "") == 0)
                if empty and column_from_1 == column_to_1:
                    if column_from_1 not in column_disabled_dict:
                        column_disabled_dict[column_from_1] = True
                elif (not empty) and column_from_1 == column_to_1:
                    column_disabled_dict[column_from_1] = False
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
                "#fff0f0" if this_kishi.woman else "#f9f9f9",
                False,
                (True, True, True, True),
                kishi_display_name_len
            )
            table_pos_all.append(t2)
            match_icons = ""
            match_icons_len = 0
            for match in this_node.series:
                if len(this_node.series) > 1:
                    if match.black_name == kishi_data.query_kishi_from_id(k).fullname:
                        black_or_white = "black"
                    elif match.white_name == kishi_data.query_kishi_from_id(k).fullname:
                        black_or_white = "white"
                match_icon = ""
                match_icon_len = 0
                match_icon += ("[[千日手|千]]" * match.sennichite)
                match_icon_len += match.sennichite
                match_icon += ("[[持将棋|持]]" * match.mochishogi)
                match_icon_len += match.mochishogi
                if match.sennichite == 0 and match.mochishogi == 0 and match.win_loss_for_black == 0:
                    match_icon = "無"
                    match_icon_len += 1
                elif match.forfeit_active:
                    if black_or_white == "black" and match.win_loss_for_black > 0:
                        match_icon += "□"
                    elif black_or_white == "white" and match.win_loss_for_black < 0:
                        match_icon += "□"
                    else:
                        match_icon += "■"
                    match_icon_len += 1
                else:
                    if black_or_white == "black" and match.win_loss_for_black > 0:
                        match_icon += "○"
                    elif black_or_white == "white" and match.win_loss_for_black < 0:
                        match_icon += "○"
                    elif black_or_white == "black" and match.win_loss_for_black < 0:
                        match_icon += "●"
                    elif black_or_white == "white" and match.win_loss_for_black > 0:
                        match_icon += "●"
                    match_icon_len += 1
                match_icons += match_icon
                match_icons_len += match_icon_len
            t3 = table_desc.TableDesc(
                (position_dicts[j][k], factor * (a - j - 1) + 3),
                (position_dicts[j][k] + 1, factor * (a - j - 1) + 3),
                False,
                match_icons,
                "#fff0f0" if this_kishi.woman else "#f9f9f9",
                False,
                (True, True, True, True),
                match_icons_len
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
                    "#fff0f0" if this_kishi.woman else "#f9f9f9",
                    False,
                    (True, True, True, True),
                    len(out_seed_text) * 1.2 if len(out_seed_text) >= 3 else len(out_seed_text)
                )
                column_num = factor * (a - j - 1) + 4
                empty = (len(out_seed_text) == 0)
                if empty:
                    if column_num not in column_disabled_dict:
                        column_disabled_dict[column_num] = True
                else:
                    column_disabled_dict[column_num] = False
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
    # pad 0+sort
    table_pos_all = table_desc.padding_0(table_pos_all)
    return organized_tab.OrganizedTable(table_pos_all, column_disabled_dict)


def draw_table(in_table_list: list, table_name: str = '') -> str:
    print(f"Begin generating table of {table_name}")
    return_block = f"<!-- Begin Bracket of {table_name}-->\n"
    row_limit = max([cell.to_cell[0] for cell in in_table_list]) + 1
    column_limit = max([cell.to_cell[1] for cell in in_table_list]) + 1
    # for row 0
    return_block += '{| border="0" cellpadding="0" cellspacing="0" style="font-size: 70%;"\n'
    # column names
    in_table_list_cur_index = 0
    while True:
        current_cell = in_table_list[in_table_list_cur_index]
        if current_cell.from_cell[0] > 0:
            break
        if not current_cell.empty:
            return_block += (f'| align="center" colspan="'
                             f'{current_cell.to_cell[1] - current_cell.from_cell[1] + 1}'
                             f'" style="border:1px solid #aaa;" bgcolor="'
                             f'{current_cell.bg_color}" |'
                             f'{current_cell.content if len(current_cell.content) > 0 else "01回戦"}\n')
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

    return_block += ("|}\n<!-- End Bracket of "
                     + f"{table_name}"
                     + "-->\n")
    return return_block


def draw_table_with_col_dis_dic(in_table_list_org_tab: organized_tab.OrganizedTable,
                                table_name: str = '',
                                default_round_name: str = '01回戦') -> str:
    in_table_list_org_tab.process_disabled_dict()
    in_table_list = in_table_list_org_tab.table_list
    print(f"Begin generating table of {table_name}")
    return_block = f"<!-- Begin Bracket of {table_name}-->\n"
    row_limit = max([cell.to_cell[0] for cell in in_table_list]) + 1
    column_limit = max([cell.to_cell[1] for cell in in_table_list]) + 1
    # for row 0
    return_block += '{| border="0" cellpadding="0" cellspacing="0" style="font-size: 70%;"\n'
    # column names
    in_table_list_cur_index = 0
    while True:
        current_cell = in_table_list[in_table_list_cur_index]
        if current_cell.from_cell[0] > 0:
            break
        if not current_cell.empty:
            return_block += (f'| align="center" colspan="'
                             f'{current_cell.to_cell[1] - current_cell.from_cell[1] + 1}'
                             f'" style="border:1px solid #aaa;" bgcolor="'
                             f'{current_cell.bg_color}" |'
                             f'{current_cell.content if len(current_cell.content) > 0 else default_round_name}\n')
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

    return_block += ("|}\n<!-- End Bracket of "
                     + f"{table_name}"
                     + "-->\n")
    return return_block
