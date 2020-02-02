from datetime import date
from metastruct import kishi_data


class LeagueInfo:
    kishi: kishi_data.Kishi = None,
    round_num: int = 0,
    output_details: list = [],
    output_detail_lengths: list = []
    wins: int = 0,
    draws: int = 0,
    losses: int = 0
    last_match_date: date = date.fromisoformat("1900-01-01")

    def __init__(self,
                 kishi,
                 round_num,
                 output_details,
                 output_detail_lengths,
                 wins,
                 draws,
                 losses,
                 last_match_date):
        self.kishi = kishi
        self.round_num = round_num
        self.output_details = output_details
        self.output_detail_lengths = output_detail_lengths
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.last_match_date = last_match_date

    def __str__(self) -> str:
        out_str_item = [
            self.kishi.fullname,
            str(self.round_num),
            str(self.output_details),
            str(self.output_detail_lengths),
            str(self.wins),
            str(self.draws),
            str(self.losses),
            date.isoformat(self.last_match_date)]
        return ",".join(out_str_item)
