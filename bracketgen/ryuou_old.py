from metastruct import organized_t, seeds_out_in, table_feed
from importdata import sql_read, gen_round_name


def ryuou_old_str(iteration: str) -> str:
    return_result = ""
    letter_list = []
    for i in range(64, 90):
        letter_list.append(chr(i + 1))
    for i in range(96, 122):
        letter_list.append(chr(i + 1))
    katakana_list = [
        'イ', 'ロ', 'ハ', 'ニ', 'ホ', 'ヘ', 'ト',
        'チ', 'リ', 'ヌ', 'ル', 'ヲ', 'ワ', 'カ',
        'ヨ', 'タ', 'レ', 'ソ', 'ツ', 'ネ', 'ナ',
        'ラ', 'ム', 'ウ', 'ヰ', 'ノ', 'オ', 'ク',
        'ヤ', 'マ', 'ケ', 'フ', 'コ', 'エ', 'テ',
        'ア', 'サ', 'キ', 'ユ', 'メ', 'ミ', 'シ',
        'ヱ', 'ヒ', 'モ', 'セ', 'ス',
    ]
    hiragana_list = [
        'あ',	'い',	'う',	'え',	'お',
        'か',	'き',	'く',	'け',	'こ',
        'さ',	'し',	'す',	'せ',	'そ',
        'た',	'ち',	'つ',	'て',	'と',
        'な',	'に',	'ぬ',	'ね',	'の',
        'は',	'ひ',	'ふ',	'へ',	'ほ',
        'ま',	'み',	'む',	'め',	'も',
        'や',	'ゆ',	'よ',
        'ら',	'り',	'る',	'れ',	'ろ',
        'わ',	'ゐ',	'ゑ',	'を',

    ]
    number_list = list(range(64))

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
            feed_0 = table_feed.TableFeed(organized_t.OrganizedTree(match_db_0,
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
            s = seeds_out_in.Seed(-2, [org_tree_normal, ], [org_tree_3, ], letter_list)
            s.assign_seed()
            feed_normal = table_feed.TableFeed(org_tree_normal,
                                               "==1組==\n===ランキング戦===\n",
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
            s = seeds_out_in.Seed(-2, [org_tree_normal, ], [org_tree_promo, ], letter_list)
            s.assign_seed()
            feed_normal = table_feed.TableFeed(org_tree_normal,
                                               f"=={i}組==\n===ランキング戦===\n",
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
                                              False,
                                              i == 6,
                                              "△",
                                              "")
            feeds_i.append(feed_normal)
            feeds_i.append(feed_promo)
        if i != 0:
            a, b = get_x_group_remain_war_trees(iteration, i)
            if a is None:
                # remain_war_disabled_flag = True
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
                    s_l = seeds_out_in.Seed(5, [feed_promo.tree, ], [], [], None, losers_dict)
                else:
                    s_l = seeds_out_in.Seed(5, [feed_3.tree, ], [], [], None, losers_dict)
                s_l.assign_seed()
                pass  # trigger 无残留决定战时的降级
            elif b is None:
                s = seeds_out_in.Seed(-2, [feeds_i[1].tree, ], [a, ], katakana_list)
                s.assign_seed()
                a_losers = a.get_runners_up() + a.get_others()
                losers_dict = dict()
                for loser in a_losers:
                    losers_dict[loser.id] = "▼"
                s_l = seeds_out_in.Seed(5, [a, ], [], [], None, losers_dict)
                s_l.assign_seed()
                feed_remain = table_feed.TableFeed(a,
                                                   f"===残留決定戦===\n▼:降級\n",
                                                   "竜王戦",
                                                   iteration,
                                                   False,
                                                   False,
                                                   "◇",
                                                   "")
                feeds_i.append(feed_remain)
            else:
                s = seeds_out_in.Seed(-2, [feeds_i[1].tree, ], [a, b, ], katakana_list)
                s.assign_seed()
                s2 = seeds_out_in.Seed(-1, [a, ], [b, ], hiragana_list)
                s2.assign_seed()
                b_losers = b.get_runners_up() + b.get_others()
                losers_dict = dict()
                for loser in b_losers:
                    losers_dict[loser.id] = "▼"
                s_l = seeds_out_in.Seed(5, [b, ], [], [], None, losers_dict)
                s_l.assign_seed()
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
        feeds_x.append(feeds_i)
    s = seeds_out_in.Seed(1, [feeds_x[1][0].tree, ], [feeds_x[0][0].tree, ], ["優勝(決勝Ｔ)", ], ["1組優勝", ])
    s.assign_seed()
    s = seeds_out_in.Seed(2, [feeds_x[1][0].tree, ], [feeds_x[0][0].tree, ], ["2位(決勝Ｔ)", ], ["1組2位", ])
    s.assign_seed()

    for j in range(len(feeds_x)):
        return_result += table_feed.draw_table_from_feed(feeds_x[j])
    return return_result


def get_x_group_normal_tree(iteration: str, group_num: int):
    match_db = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "ランキング戦")
    round_db = gen_round_name.read_round("竜王戦", iteration, f"{group_num}組", "ランキング戦")
    org_tree = organized_t.OrganizedTree(match_db, f"{group_num}組ランキング戦", round_db)
    return org_tree


def get_x_group_promo_round_tree(iteration: str, group_num: int):
    match_db = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "昇級者決定戦")
    round_db = gen_round_name.read_round("竜王戦", iteration, f"{group_num}組", "昇級者決定戦")
    org_tree = organized_t.OrganizedTree(match_db, f"{group_num}組昇級者決定戦", round_db)
    return org_tree


def get_1_group_appear_round_tree(iteration: str, pos_num: int):
    match_db = sql_read.read_match("竜王戦", iteration, "1組", f"{pos_num}位出場者決定戦")
    round_db = gen_round_name.read_round("竜王戦", iteration, "1組", f"{pos_num}位出場者決定戦")
    org_tree = organized_t.OrganizedTree(match_db, f"1組{pos_num}位出場者決定戦", round_db)
    return org_tree


def get_x_group_remain_war_trees(iteration: str, group_num: int) -> tuple:
    match_db = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "残留決定戦")
    if len(match_db) == 0:
        return None, None
    match_db_first_round = sql_read.read_match("竜王戦", iteration, f"{group_num}組", "残留決定戦", "01回戦")
    if len(match_db_first_round) == 0:  # match_db only have first round
        org_tree = organized_t.OrganizedTree(match_db, f"{group_num}組残留決定戦", ["", ])
        return org_tree, None
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
        org_tree_1 = organized_t.OrganizedTree(match_db_first_round, f"{group_num}組残留決定戦", ["01回戦", ])
        round_db = gen_round_name.read_round("竜王戦", iteration, f"{group_num}組", "残留決定戦")
        org_tree_2 = organized_t.OrganizedTree(match_db_non_first_round, f"{group_num}組残留決定戦", round_db[:-1])
        return org_tree_1, org_tree_2
    else:
        round_db = gen_round_name.read_round("竜王戦", iteration, f"{group_num}組", "残留決定戦")
        org_tree = organized_t.OrganizedTree(match_db, f"{group_num}組残留決定戦", round_db)
        return org_tree, None
