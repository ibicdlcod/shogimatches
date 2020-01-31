from bracketgen import title_match, str_list
from metastruct import organized_tr, seeds_out_in, table_feed
from importdata import sql_read, gen_round_name


def ryuou_old_str_dict(iteration: str, iteration_last: str = None) -> dict:
    return_dict = dict()
    letter_list = str_list.letter_list
    katakana_list = str_list.katakana_list
    hiragana_list = str_list.hiragana_list
    number_list = str_list.number_list
    title_matches = sql_read.read_match("竜王戦", iteration, "タイトル戦", "七番勝負")
    if iteration_last is not None:
        title_matches_last = sql_read.read_match("竜王戦", iteration_last, "タイトル戦", "七番勝負")
        org_tree_title_last = organized_tr.OrganizedTree(title_matches_last, f"タイトル戦七番勝負", ["", ])
    else:
        org_tree_title_last = None
    org_tree_title = organized_tr.OrganizedTree(title_matches, f"タイトル戦七番勝負", ["", ])
    return_dict[7] = title_match.title_match_str(org_tree_title,
                                                 "竜王戦",
                                                 iteration,
                                                 "竜王",
                                                 "七番勝負",
                                                 org_tree_title_last)
    legend_string = ('{| border="1" class="wikitable" style="font-size:89%"\n|\n'
                     '◎：決勝進出　△：昇級　◇：残留 ▼：降級\n|}\n')
    feeds_x = []
    for i in range(0, 7):
        feeds_i = []
        remain_war_disabled_flag = False
        feed_normal = None
        feed_promo = None
        feed_3 = None
        if i == 0:
            match_db_0 = sql_read.read_match("竜王戦", iteration, "決勝トーナメント")
            round_db_0 = gen_round_name.read_round("竜王戦", iteration, "決勝トーナメント")
            feed_0 = table_feed.TableFeed(organized_tr.OrganizedTree(match_db_0,
                                                                     "決勝トーナメント",
                                                                     round_db_0),
                                          "==決勝トーナメント==\n",
                                          "竜王戦",
                                          iteration,
                                          True,
                                          False,
                                          "◎",
                                          "")
            feeds_i.append(feed_0)
        elif i == 1:
            org_tree_normal = get_x_group_normal_tree(iteration, 1)
            org_tree_3 = get_1_group_appear_round_tree(iteration, 3)
            seeds_out_in.Seed(-2, [org_tree_normal, ], [org_tree_3, ], letter_list)
            feed_normal = table_feed.TableFeed(org_tree_normal,
                                               "==1組==\n" + legend_string + "===ランキング戦===\n",
                                               "竜王戦",
                                               iteration,
                                               False,
                                               True,
                                               "◎",
                                               "◎")
            feed_3 = table_feed.TableFeed(org_tree_3,
                                          "===3位出場者決定戦===\n",
                                          "竜王戦",
                                          iteration,
                                          False,
                                          remain_war_disabled_flag,
                                          "◎",
                                          "◎")
            feeds_i.append(feed_normal)
            feeds_i.append(feed_3)
        else:
            org_tree_normal = get_x_group_normal_tree(iteration, i)
            org_tree_promo = get_x_group_promo_round_tree(iteration, i)
            seeds_out_in.Seed(-2, [org_tree_normal, ], [org_tree_promo, ], letter_list)
            feed_normal = table_feed.TableFeed(org_tree_normal,
                                               f"=={i}組==\n" + legend_string + "===ランキング戦===\n",
                                               "竜王戦",
                                               iteration,
                                               False,
                                               True,
                                               "◎",
                                               "◎" if i < 4 else "△")
            feed_promo = table_feed.TableFeed(org_tree_promo,
                                              "===昇級者決定戦===\n",
                                              "竜王戦",
                                              iteration,
                                              i == 6,
                                              False,
                                              "△",
                                              "")
            feeds_i.append(feed_normal)
            feeds_i.append(feed_promo)
        if i != 0:
            a, b, c = get_x_group_remain_war_trees(iteration, i)
            if a is None:
                if i != 6:
                    if feed_promo is not None:
                        feed_promo.prefix = "===昇級者決定戦===\n▼:降級\n"
                    else:  # to 5 for new
                        feed_3.prefix = "===3位出場者決定戦===\n▼:降級\n"
                normal_first_round_losers = feed_normal.tree.get_losers_in_their_first()
                if feed_promo is not None:
                    promo_first_round_losers = feed_promo.tree.get_losers_in_their_first()
                else:
                    promo_first_round_losers = feed_3.tree.get_losers_in_their_first()
                relegated = []
                for loser in promo_first_round_losers:
                    if loser in normal_first_round_losers:
                        relegated.append(loser)
                losers_dict = dict()
                for loser in relegated:
                    losers_dict[loser.id] = "▼"
                if feed_promo is not None:
                    seeds_out_in.Seed(5, [feed_promo.tree, ], [], [], None, losers_dict)
                else:
                    seeds_out_in.Seed(5, [feed_3.tree, ], [], [], None, losers_dict)
                pass  # trigger 无残留决定战时的降级
            elif b is None:
                seeds_out_in.Seed(-2, [feeds_i[1].tree, ], [a, ], katakana_list)
                a_losers = a.get_runners_up() + a.get_others()
                losers_dict = dict()
                for loser in a_losers:
                    losers_dict[loser.id] = "▼"
                seeds_out_in.Seed(5, [a, ], [], [], None, losers_dict)
                feed_remain = table_feed.TableFeed(a,
                                                   f"===残留決定戦===\n▼:降級\n",
                                                   "竜王戦",
                                                   iteration,
                                                   False,
                                                   False,
                                                   "◇",
                                                   "")
                feeds_i.append(feed_remain)
            elif c is None:
                seeds_out_in.Seed(-2, [feeds_i[1].tree, ], [a, b, ], katakana_list)
                seeds_out_in.Seed(-1, [a, ], [b, ], hiragana_list)
                b_losers = b.get_runners_up() + b.get_others()
                losers_dict = dict()
                for loser in b_losers:
                    losers_dict[loser.id] = "▼"
                seeds_out_in.Seed(5, [b, ], [], [], None, losers_dict)
                feed_remain = table_feed.TableFeed(a,
                                                   f"===残留決定戦===\n▼:降級\n",
                                                   "竜王戦",
                                                   iteration,
                                                   False,
                                                   False,
                                                   "◇",
                                                   "")
                feed_remain2 = table_feed.TableFeed(b,
                                                    f"<br/>",
                                                    "竜王戦",
                                                    iteration,
                                                    False,
                                                    False,
                                                    "◇",
                                                    "")
                feeds_i.append(feed_remain)
                feeds_i.append(feed_remain2)
            else:
                seeds_out_in.Seed(-2, [feeds_i[1].tree, ], [a, b, c, ], katakana_list)
                seeds_out_in.Seed(-1, [a, ], [b, ], hiragana_list)
                seeds_out_in.Seed(-1, [b, ], [c, ], number_list)
                c_losers = c.get_runners_up() + c.get_others()
                losers_dict = dict()
                for loser in c_losers:
                    losers_dict[loser.id] = "▼"
                seeds_out_in.Seed(5, [c, ], [], [], None, losers_dict)
                feed_remain = table_feed.TableFeed(a,
                                                   f"===残留決定戦===\n▼:降級\n",
                                                   "竜王戦",
                                                   iteration,
                                                   False,
                                                   False,
                                                   "◇",
                                                   "")
                feed_remain2 = table_feed.TableFeed(b,
                                                    f"<br/>",
                                                    "竜王戦",
                                                    iteration,
                                                    False,
                                                    False,
                                                    "◇",
                                                    "")
                feed_remain3 = table_feed.TableFeed(c,
                                                    f"<br/>",
                                                    "竜王戦",
                                                    iteration,
                                                    False,
                                                    False,
                                                    "◇",
                                                    "")
                feeds_i.append(feed_remain)
                feeds_i.append(feed_remain2)
                feeds_i.append(feed_remain3)
        feeds_x.append(feeds_i)
    tree_0 = feeds_x[0][0].tree
    if iteration == "第01期":
        seeds_out_in.Seed(0, [], [tree_0, ], [], [], {165: "第26期十段", 115: "永世十段", 42: "永世十段"})
    seeds_out_in.Seed(1, [feeds_x[1][0].tree, ], [tree_0, ], ["優勝(決勝Ｔ)", ], ["1組優勝", ])
    seeds_out_in.Seed(2, [feeds_x[1][0].tree, ], [tree_0, ], ["2位(決勝Ｔ)", ], ["1組2位", ])
    seeds_out_in.Seed(1, [feeds_x[1][1].tree, ], [tree_0, ], ["3位(決勝Ｔ)", "3位(決勝Ｔ)", ], ["1組3位", "1組3位", ])
    seeds_out_in.Seed(1, [feeds_x[2][0].tree, ], [tree_0, ], ["優勝(決勝Ｔ)·昇級", ], ["2組優勝", ])
    seeds_out_in.Seed(2, [feeds_x[2][0].tree, ], [tree_0, ], ["2位(決勝Ｔ)·昇級", ], ["2組2位", ])
    seeds_out_in.Seed(1, [feeds_x[3][0].tree, ], [tree_0, ], ["優勝(決勝Ｔ)·昇級", ], ["3組優勝", ])
    seeds_out_in.Seed(2, [feeds_x[3][0].tree, ], [tree_0, ], ["2位(決勝Ｔ)·昇級", ], ["3組2位", ])
    seeds_out_in.Seed(1, [feeds_x[4][0].tree, ], [tree_0, ], ["優勝(決勝Ｔ)·昇級", ], ["4組優勝", ])
    seeds_out_in.Seed(1, [feeds_x[5][0].tree, ], [tree_0, ], ["優勝(決勝Ｔ)·昇級", ], ["5組優勝", ])
    seeds_out_in.Seed(1, [feeds_x[6][0].tree, ], [tree_0, ], ["優勝(決勝Ｔ)·昇級", ], ["6組優勝", ])
    for i in range(4, 7):
        loser_dict = dict()
        for loser in feeds_x[i][0].tree.get_runners_up():
            loser_dict[loser.id] = "昇級"
        seeds_out_in.Seed(5, [feeds_x[i][0].tree, ], [], [], [], loser_dict)
    for i in range(2, 7):
        winner_dict = dict()
        for winner in feeds_x[i][1].tree.get_winners():
            winner_dict[winner.id] = "昇級"
        seeds_out_in.Seed(5, [feeds_x[i][1].tree, ], [], [], [], winner_dict)
    challenge_dict = dict()
    for kishi in tree_0.get_winners():
        challenge_dict[kishi.id] = "挑戦者"
    seeds_out_in.Seed(5, [tree_0, ], [], [], [], challenge_dict)

    for j in range(len(feeds_x)):
        return_dict[j] = table_feed.draw_table_from_feed(feeds_x[j])
    return return_dict


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
        print("Irregular remain war tree found")
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
            print("Irregular remain war tree found")
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
