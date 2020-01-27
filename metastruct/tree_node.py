from metastruct import kishi_data


class TreeNode:
    black_of_first: kishi_data.Kishi = None,
    white_of_first: kishi_data.Kishi = None
    title_holder = None  # "black" or "white" or None
    superior_1win_advantage = None  # "black" or "white" or None
    series = []  # a list of matches
    advance_result = 0  # >0 for black and <0 for white
    black_qualified_from = None  # its a TreeNode
    white_qualified_from = None  # its a TreeNode
    black_seed_in: str = None
    white_seed_in: str = None
    black_seed_out: str = None
    white_seed_out: str = None

    def __init__(self, match_list: list, title_holder: kishi_data.Kishi = None,
                 superior_1win_advantange: kishi_data.Kishi = None):
        if len(match_list) == 0:
            print("Invalid: no match specified for TreeNode")
            exit(2)
        series_matches = match_list
        series_matches.sort(key=lambda match1: match1.match_date)
        self.black_of_first = kishi_data.query_kishi_from_name(series_matches[0].black_name)
        self.white_of_first = kishi_data.query_kishi_from_name(series_matches[0].white_name)
        black_adv = 0
        if superior_1win_advantange is not None:
            if superior_1win_advantange.id == self.black_of_first.id:
                black_adv = 1
            elif superior_1win_advantange.id == self.white_of_first.id:
                black_adv = -1
        self.advance_result = black_adv
        for match2 in series_matches:
            if match2.black_name == self.black_of_first.fullname:
                self.advance_result += match2.win_loss_for_black
            elif match2.white_name == self.black_of_first.fullname:
                self.advance_result -= match2.win_loss_for_black
        # basics done
