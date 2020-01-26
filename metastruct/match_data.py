from datetime import date
import hashlib


class Match:
    # defaults
    hash: bytearray
    fiscal_year: int = 1900
    match_date: date = date.fromisoformat("1900-01-01")
    win_loss_for_black: int = 1  # 1=victory -1=defeat 0=draw
    forfeit_active: bool = False
    black_name: str = ""
    white_name: str = ""
    iteration: str = ""
    tournament_name: str = ""
    detail1: str = ""
    detail2: str = ""
    detail3: str = ""
    mochishogi: int = 0
    sennichite: int = 0

    # init begin
    def __init__(self,
                 i_fiscal_year: int,
                 i_match_date: date,
                 i_win_loss_black: int,
                 i_forfeit: bool,
                 i_black: str,
                 i_white: str,
                 i_iter: str,
                 i_tournament: str,
                 i_detail1: str,
                 i_detail2: str,
                 i_detail3: str,
                 i_mochishogi: int,
                 i_sennichite: int
                 ):
        match_code = (i_match_date.isoformat()
                      + i_black + "vs" + i_white)
        h = hashlib.sha512()
        h.update(bytes(match_code, "utf-8"))
        self.hash = h.digest()
        self.fiscal_year = i_fiscal_year
        self.match_date = i_match_date
        self.win_loss_for_black = i_win_loss_black
        self.forfeit_active = i_forfeit
        self.black_name = i_black
        self.white_name = i_white
        self.iteration = i_iter
        self.tournament_name = i_tournament
        self.detail1 = i_detail1
        self.detail2 = i_detail2
        self.detail3 = i_detail3
        self.mochishogi = i_mochishogi
        self.sennichite = i_sennichite

    def __str__(self) -> str:
        out_str_item = [str(self.hash.hex()),
                        str(self.fiscal_year),
                        str(self.match_date.isoformat()),
                        str(self.win_loss_for_black),
                        str(self.forfeit_active),
                        self.black_name,
                        self.white_name,
                        self.iteration,
                        self.tournament_name,
                        self.detail1,
                        self.detail2,
                        self.detail3,
                        str(self.mochishogi),
                        str(self.sennichite)]
        return ",".join(out_str_item)