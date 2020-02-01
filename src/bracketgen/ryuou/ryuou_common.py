from bracketgen import gen_round_name
from importdata import sql_read
from metastruct import organized_tr


def get_x_group_normal_tree(iteration: str, group_num: int):
    match_db = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "ランキング戦")
    round_db = gen_round_name.read_round("竜王戦", iteration, f"{group_num}組", "ランキング戦")
    org_tree = organized_tr.OrganizedTree(match_db, f"{group_num}組ランキング戦", round_db)
    return org_tree


def get_x_group_promo_round_tree(iteration: str, group_num: int):
    match_db = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "昇級者決定戦")
    match_db_last_round = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "昇級者決定戦", "決勝")
    last_round_losers = []
    for match in match_db_last_round:
        if match.win_loss_for_black > 0:
            last_round_losers.append(match.white_name)
        elif match.win_loss_for_black < 0:
            last_round_losers.append(match.black_name)
    irregular_promo_matches = []
    irregular_promo_flag = False
    for match in match_db_last_round:
        if match.win_loss_for_black > 0:
            winner = match.black_name
        elif match.win_loss_for_black < 0:
            winner = match.white_name
        else:
            winner = None
        if winner in last_round_losers:
            irregular_promo_flag = True
            irregular_promo_matches.append(match)
    regular_promo_matches = match_db
    for match in irregular_promo_matches:
        regular_promo_matches.remove(match)
    round_db = gen_round_name.read_round("竜王戦", iteration, f"{group_num}組", "昇級者決定戦")
    if not irregular_promo_flag:
        org_tree = organized_tr.OrganizedTree(match_db, f"{group_num}組昇級者決定戦", round_db)
        return org_tree, None
    else:
        print("Irregular promo war tree (2nd degree) found")
        org_tree_0 = organized_tr.OrganizedTree(regular_promo_matches, f"{group_num}組昇級者決定戦", round_db)
        org_tree_1 = organized_tr.OrganizedTree(irregular_promo_matches, f"{group_num}組昇級者決定戦", ["決勝"])
        return org_tree_0, org_tree_1


def get_1_group_appear_round_tree(iteration: str, pos_num: int):
    match_db = sql_read.read_match("竜王戦", iteration, "1組", f"{pos_num}位出場者決定戦")
    round_db = gen_round_name.read_round("竜王戦", iteration, "1組", f"{pos_num}位出場者決定戦")
    org_tree = organized_tr.OrganizedTree(match_db, f"1組{pos_num}位出場者決定戦", round_db)
    return org_tree


def get_x_group_remain_war_trees(iteration: str, group_num: int) -> tuple:
    match_db = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "残留決定戦")
    if len(match_db) == 0:
        return None, None, None
    match_db_first_round = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "残留決定戦", "01回戦")
    if len(match_db_first_round) == 0:  # match_db only have first round
        org_tree = organized_tr.OrganizedTree(match_db, f"{group_num}組残留決定戦", ["", ])
        return org_tree, None, None
    first_round_one_match = match_db_first_round[0]
    first_round_loser_0 = None
    if first_round_one_match.win_loss_for_black > 0:
        first_round_loser_0 = first_round_one_match.white_name
    elif first_round_one_match.win_loss_for_black < 0:
        first_round_loser_0 = first_round_one_match.black_name
    else:
        print("Remain war first round should have a decisive result")
        exit(3)
    match_db_non_first_round = []
    for m in match_db:
        if m not in match_db_first_round:
            match_db_non_first_round.append(m)
    non_first_round_participants = []
    for m in match_db_non_first_round:
        non_first_round_participants.append(m.black_name)
        non_first_round_participants.append(m.white_name)
    if first_round_loser_0 in non_first_round_participants:
        print("Irregular remain war tree (2nd degree) found")
        # confirm there are two rounds
        org_tree_1 = organized_tr.OrganizedTree(match_db_first_round, f"{group_num}組残留決定戦", ["01回戦", ])
        round_db = gen_round_name.read_round("竜王戦", iteration, f"{group_num}組", "残留決定戦")
        org_tree_2 = organized_tr.OrganizedTree(match_db_non_first_round, f"{group_num}組残留決定戦", round_db[:-1])
        match_db_second_round = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "残留決定戦", "02回戦")
        if len(match_db_second_round) == 0:
            return org_tree_1, org_tree_2, None
        second_round_one_match = match_db_second_round[0]
        second_round_loser_0 = None
        if second_round_one_match.win_loss_for_black > 0:
            second_round_loser_0 = second_round_one_match.white_name
        elif second_round_one_match.win_loss_for_black < 0:
            second_round_loser_0 = second_round_one_match.black_name
        else:
            print("Remain war second round should have a decisive result")
            exit(3)
        match_db_non_second_round = []
        for m in match_db:
            if (m not in match_db_second_round) and (m not in match_db_first_round):
                match_db_non_second_round.append(m)
        non_second_round_participants = []
        for m in match_db_non_second_round:
            non_second_round_participants.append(m.black_name)
            non_second_round_participants.append(m.white_name)
        if second_round_loser_0 in non_second_round_participants:
            print("Irregular remain war tree (3rd degree) found")
            org_tree_1 = organized_tr.OrganizedTree(match_db_first_round, f"{group_num}組残留決定戦", ["01回戦", ])
            round_db = gen_round_name.read_round("竜王戦", iteration, f"{group_num}組", "残留決定戦")
            org_tree_2 = organized_tr.OrganizedTree(match_db_second_round, f"{group_num}組残留決定戦", ["02回戦", ])
            org_tree_3 = organized_tr.OrganizedTree(
                match_db_non_second_round, f"{group_num}組残留決定戦", round_db[:-2])
            return org_tree_1, org_tree_2, org_tree_3
        else:
            return org_tree_1, org_tree_2, None
    else:
        round_db = gen_round_name.read_round("竜王戦", iteration, f"{group_num}組", "残留決定戦")
        org_tree = organized_tr.OrganizedTree(match_db, f"{group_num}組残留決定戦", round_db)
        return org_tree, None, None
