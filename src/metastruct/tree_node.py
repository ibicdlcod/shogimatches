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
    round_num: str = None
    round_num_display: str = ""

    def __init__(self, match_list: list, title_holder: kishi_data.Kishi = None,
                 superior_1win_advantage: kishi_data.Kishi = None, ):
        if len(match_list) == 0:
            print("Invalid: no match specified for TreeNode")
            exit(2)
        self.title_holder = title_holder
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
            self.round_num,
            self.round_num_display,
            "\n" + "\n".join([str(match) for match in self.series]),
        ]
        return ",".join(out_str_item)


def match_icon_for_kishi_with_length(this_node: TreeNode, kishi_id: int):
    match_icons = []
    length = 0
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
        match_icon += ("[[千日手|千]]" * match.sennichite)
        length += match.sennichite
        match_icon += ("[[持将棋|持]]" * match.mochishogi)
        length += match.mochishogi
        if match.sennichite == 0 and match.mochishogi == 0 and match.win_loss_for_black == 0:
            match_icon = "無"
            length += 1
        elif match.forfeit_active:
            if black_or_white == "black" and match.win_loss_for_black > 0:
                match_icon += "□"
            elif black_or_white == "white" and match.win_loss_for_black < 0:
                match_icon += "□"
            else:
                match_icon += "■"
            length += 1
        else:
            length += 1
            if black_or_white == "black" and match.win_loss_for_black > 0:
                match_icon += "○"
            elif black_or_white == "white" and match.win_loss_for_black < 0:
                match_icon += "○"
            elif black_or_white == "black" and match.win_loss_for_black < 0:
                match_icon += "●"
            elif black_or_white == "white" and match.win_loss_for_black > 0:
                match_icon += "●"
            else:
                length -= 1
        match_icons.append(match_icon)
    return match_icons, max(length, 0)
