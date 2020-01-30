from datetime import date
from importdata import sql_read

ryuou_end_dates = dict()
ryuou_end_dates[0] = date.fromisoformat("1900-01-01")
ryuou_winners = dict()
for i in range(1, 9):
    iteration = "第" + str(i).zfill(2) + "期"
    ryuou_matches = sql_read.read_match("竜王戦", iteration, "タイトル戦", "七番勝負")
    ryuou_matches.sort(key=lambda x: x.match_date)
    end_date = ryuou_matches[-1].match_date
    ryuou_end_dates[i] = end_date
    ryuou_winners[i] = (ryuou_matches[-1].black_name if ryuou_matches[-1].win_loss_for_black > 0
                        else ryuou_matches[-1].white_name)

ryuou_end_dates[9] = date.fromisoformat("2100-01-01")
ryuou_winners[7] = None
ryuou_winners[8] = None
# for i in range(13, 53):
#     iteration = "第" + str(i).zfill(2) + "期"
#     meijin_matches = sql_read.read_match("名人戦", iteration, "タイトル戦", "七番勝負")
meijin_end_dates = dict()
meijin_end_dates[12] = date.fromisoformat("1900-01-01")
meijin_winners = dict()
for i in range(13, 54):
    iteration = "第" + str(i).zfill(2) + "期"
    meijin_matches = sql_read.read_match("名人戦", iteration, "タイトル戦", "七番勝負")
    meijin_matches.sort(key=lambda x: x.match_date)
    end_date = meijin_matches[-1].match_date
    meijin_end_dates[i] = end_date
    meijin_winners[i] = (meijin_matches[-1].black_name if meijin_matches[-1].win_loss_for_black > 0
                         else meijin_matches[-1].white_name)
meijin_end_dates[54] = date.fromisoformat("2100-01-01")
meijin_winners[52] = None
meijin_winners[53] = None


def import_former_ryuou(in_date: date = date.fromisoformat("1900-01-01")):
    current_ryuou_iteration = 0
    while in_date >= ryuou_end_dates[current_ryuou_iteration + 1]:
        current_ryuou_iteration += 1
    former_ryuou_iteration = current_ryuou_iteration - 1
    if former_ryuou_iteration <= 0:
        return None
    else:
        return ryuou_winners[former_ryuou_iteration]
    

def import_former_meijin(in_date: date = date.fromisoformat("1900-01-01")):
    current_meijin_iteration = 11
    while in_date >= meijin_end_dates[current_meijin_iteration + 1]:
        current_meijin_iteration += 1
    former_meijin_iteration = current_meijin_iteration - 1
    if former_meijin_iteration <= 12:
        return None
    else:
        return meijin_winners[former_meijin_iteration]