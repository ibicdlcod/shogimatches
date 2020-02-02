from datetime import date
from metastruct import tree_node, league_info


def generate_lea_pos(match_db: list,
                     junni_dict: dict = None,
                     round_names: list = None,
                     round_names_prefix: str = None) -> list:
    first_two_rounds = []
    node_db = dict()
    round_names_with_prefix = []
    for round_name in round_names:
        node_db[round_name] = []
        round_names_with_prefix.append(round_names_prefix + round_name)
    for match in match_db:
        match_node = tree_node.TreeNode([match, ], )
        match_node_index = round_names_with_prefix.index(match_node.round_num)
        node_db[round_names[match_node_index]].append(match_node)
        if match_node_index == 0 or match_node_index == 1:
            first_two_rounds.append(match_node)
    participants = set()
    for node in first_two_rounds:
        participants.add(node.black_of_first)
        participants.add(node.white_of_first)
    participants = list(participants)

    kishi_surname_dict = dict()
    for this_kishi in participants:
        this_kishi_surname = this_kishi.fullname[:this_kishi.surname_length]
        kishi_surname_dict[this_kishi.id] = this_kishi_surname
    kishi_surname_dict2 = dict()
    for this_kishi in participants:
        this_kishi_surname = this_kishi.fullname[:this_kishi.surname_length]
        if list(kishi_surname_dict.values()).count(this_kishi_surname) > 1:
            this_kishi_surname2 = this_kishi.fullname[:this_kishi.surname_length + 1]
            kishi_surname_dict2[this_kishi.id] = this_kishi_surname2
        else:
            kishi_surname_dict2[this_kishi.id] = kishi_surname_dict[this_kishi.id]

    all_kishi_output = dict()
    all_kishi_output_len = dict()
    kishi_wins_output = dict()
    kishi_draws_output = dict()
    kishi_loses_output = dict()
    kishi_last_match_date = dict()
    kishi_league_information = []
    for kishi in participants:
        all_kishi_output[kishi] = []
        all_kishi_output_len[kishi] = []
        kishi_wins_output[kishi] = 0
        kishi_draws_output[kishi] = 0
        kishi_loses_output[kishi] = 0
        kishi_last_match_date[kishi] = date.fromisoformat("1900-01-01")
        for i in range(len(round_names)):  # query match
            this_nodes = [node for node in node_db[round_names[i]]]
            node_contains_self = None
            opponent_id = 0
            for node in this_nodes:
                if node.black_of_first == kishi:
                    opponent_id = node.white_of_first.id
                    node_contains_self = node
                elif node.white_of_first == kishi:
                    opponent_id = node.black_of_first.id
                    node_contains_self = node
            if node_contains_self is not None:
                icon_str_list, length = tree_node.match_icon_for_kishi_with_length(node_contains_self, kishi.id)
                opponent_display_name = kishi_surname_dict2[opponent_id]
                this_cell_output = icon_str_list[0] + opponent_display_name
                this_cell_output_len = length + len(opponent_display_name)
                winner = node_contains_self.winner()
                if winner is None:
                    kishi_draws_output[kishi] += 1
                elif winner == kishi:
                    kishi_wins_output[kishi] += 1
                else:
                    kishi_loses_output[kishi] += 1
                kishi_last_match_date[kishi] = max(kishi_last_match_date[kishi],
                                                   node_contains_self.series[0].match_date)
            else:
                this_cell_output = "－－－"
                this_cell_output_len = 3
            all_kishi_output[kishi].append(this_cell_output)
            all_kishi_output_len[kishi].append(this_cell_output_len)
    if junni_dict is None:
        participants.sort(key=lambda x: (kishi_wins_output[x], - kishi_loses_output[x], - x.id), reverse=True)
    else:
        participants.sort(key=lambda x: (kishi_wins_output[x],
                                         - kishi_loses_output[x],
                                         (- 99) if (x.id not in junni_dict.keys()) else (- junni_dict[x.id]),
                                         - x.id), reverse=True)
    for kishi in participants:
        kishi_league_information.append(league_info.LeagueInfo(
            kishi,
            len(round_names),
            all_kishi_output[kishi],
            all_kishi_output_len[kishi],
            kishi_wins_output[kishi],
            kishi_draws_output[kishi],
            kishi_loses_output[kishi],
            kishi_last_match_date[kishi]
        ))
    return kishi_league_information
