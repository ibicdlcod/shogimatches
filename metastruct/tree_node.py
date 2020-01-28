from metastruct import kishi_data


class TreeNode:
    black_of_first: kishi_data.Kishi = None,
    white_of_first: kishi_data.Kishi = None
    title_holder = None  # "black" or "white" or None
    win_advantage_1 = None  # "black" or "white" or None
    series = []  # a list of matches
    advance_result = 0  # >0 for black and <0 for white
    black_q_from = None  # its a TreeNode
    white_q_from = None  # its a TreeNode
    black_seed_in: str = None
    white_seed_in: str = None
    black_seed_out: str = None
    white_seed_out: str = None
    round_num: str = None
    round_num_display: str = ""

    def __init__(self, match_list: list, title_holder: kishi_data.Kishi = None,
                 superior_1win_advantage: kishi_data.Kishi = None):
        if len(match_list) == 0:
            print("Invalid: no match specified for TreeNode")
            exit(2)
        self.series = match_list
        self.series.sort(key=lambda match1: match1.match_date)
        self.black_of_first = kishi_data.query_kishi_from_name(self.series[0].black_name)
        self.white_of_first = kishi_data.query_kishi_from_name(self.series[0].white_name)
        black_adv = 0
        if superior_1win_advantage is not None:
            if superior_1win_advantage.id == self.black_of_first.id:
                black_adv = 1
            elif superior_1win_advantage.id == self.white_of_first.id:
                black_adv = -1
        self.advance_result = black_adv
        for match2 in self.series:
            if match2.black_name == self.black_of_first.fullname:
                self.advance_result += match2.win_loss_for_black
            elif match2.white_name == self.black_of_first.fullname:
                self.advance_result -= match2.win_loss_for_black
        detail3_0: str = self.series[0].detail3
        if detail3_0.endswith("局"):
            self.round_num = self.series[0].detail1 + self.series[0].detail2
            self.round_num_display = self.series[0].detail2
        else:
            self.round_num = self.series[0].detail1 + self.series[0].detail2 \
                             + detail3_0
            self.round_num_display = detail3_0
        # basics done

    def winner(self):
        if self.advance_result > 0:
            return self.black_of_first
        elif self.advance_result < 0:
            return self.white_of_first
        else:
            return None

    def loser(self):
        if self.advance_result > 0:
            return self.white_of_first
        elif self.advance_result < 0:
            return self.black_of_first
        else:
            return None

    def __str__(self) -> str:
        out_str_item = [
            self.black_of_first.fullname,
            self.white_of_first.fullname,
            '' if self.title_holder is None else self.title_holder,
            '' if self.win_advantage_1 is None else self.win_advantage_1,
            str(self.advance_result),
            '' if self.black_q_from is None else self.black_q_from.black_of_first.fullname,
            '' if self.black_q_from is None else self.black_q_from.white_of_first.fullname,
            '' if self.white_q_from is None else self.white_q_from.black_of_first.fullname,
            '' if self.white_q_from is None else self.white_q_from.white_of_first.fullname,
            '' if self.black_seed_in is None else self.black_seed_in,
            '' if self.white_seed_in is None else self.white_seed_in,
            '' if self.black_seed_out is None else self.black_seed_out,
            '' if self.white_seed_out is None else self.white_seed_out,
            self.round_num,
            self.round_num_display,
            "\n" + "\n".join([str(match) for match in self.series]),
        ]
        return ",".join(out_str_item)
