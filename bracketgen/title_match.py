from metastruct import organized_tr, tree_node, kishi_data


def title_match_str(matches_tree: organized_tr.OrganizedTree,
                    tournament_name: str,
                    iteration: str,
                    title_name: str,
                    max_match_length: str,
                    last_matches_tree=None) -> str:
    match_node = matches_tree.last_remain_nodes[0]
    last_matches_node = last_matches_tree.last_remain_nodes[0] if last_matches_tree is not None else None
    match_length = len(match_node.series)
    if last_matches_node is not None:
        last_match_participants = last_matches_tree.get_winners()
        if (match_node.winner() not in last_match_participants) and (match_node.loser() not in last_match_participants):
            new_title_flag = True
        else:
            new_title_flag = False
    else:
        new_title_flag = True
    if new_title_flag:
        black = match_node.black_of_first
    else:
        black = last_matches_node.winner()
    black_rank = black.rank(match_node.series[0].match_date)[0]
    if black.wiki_name == "":
        black_display_name = "[[" \
                             + black.fullname \
                             + "]]" \
                             + (black_rank if last_matches_tree is None else title_name)
    else:
        black_display_name = "[[" \
                             + black.wiki_name \
                             + "|" \
                             + black.fullname \
                             + "]]" \
                             + (black_rank if last_matches_tree is None else title_name)
    if black == match_node.black_of_first:
        white = match_node.white_of_first
    else:
        white = match_node.black_of_first
    white_rank = white.rank(match_node.series[0].match_date)[0]
    if black.wiki_name == "":
        white_display_name = "[[" \
                             + white.fullname \
                             + "]]" \
                             + white_rank
    else:
        white_display_name = "[[" \
                             + black.wiki_name \
                             + "|" \
                             + black.fullname \
                             + "]]" \
                             + white_rank
    black_win_loss = match_icon_for_kishi(match_node, black.id)
    white_win_loss = match_icon_for_kishi(match_node, white.id)
    return_result = ""
    return_result += ("==" + iteration + tournament_name + max_match_length + "==\n")
    return_result += f"開催:{match_node.series[0].match_date.isoformat()} " \
                     f"- {match_node.series[-1].match_date.isoformat()}\n"
    return_result += '{| class="wikitable" style="text-align: center;"\n'
    return_result += '!対局者!!'
    for i in range(match_length):
        return_result += f'第{i+1}局!!'
    return_result += "\n|-\n"
    black_bold = ("'''" if match_node.winner() == black else "")
    return_result += "|" + black_bold + black_display_name + black_bold + "||"
    for i in range(match_length):
        return_result += black_win_loss[i] + "||"
    if last_matches_tree is not None and not new_title_flag:
        if match_node.winner() == black:
            return_result += "'''" + title_name + "位防衛'''"
    else:
        if match_node.winner() == black:
            return_result += "'''" + title_name + "位獲得'''"
    return_result += "\n|-\n"
    white_bold = ("'''" if match_node.winner() == white else "")
    return_result += "|" + white_bold + white_display_name + white_bold + "||"
    for i in range(match_length):
        return_result += white_win_loss[i] + "||"
    if last_matches_tree is not None and not new_title_flag:
        if match_node.winner() == white:
            return_result += "'''" + title_name + "位奪取'''"
    else:
        if match_node.winner() == white:
            return_result += "'''" + title_name + "位獲得'''"
    return_result += "\n|}\n"
    return_result += "<br/>\n"
    return return_result


def match_icon_for_kishi(this_node: tree_node.TreeNode, kishi_id: int):
    match_icons = []
    for match in this_node.series:
        if match.black_name == kishi_data.query_kishi_from_id(kishi_id).fullname:
            black_or_white = "black"
        elif match.white_name == kishi_data.query_kishi_from_id(kishi_id).fullname:
            black_or_white = "white"
        else:
            black_or_white = ""
            print("Kishi_id not in match participants")
            exit(3)
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
        match_icons.append(match_icon)
    return match_icons
