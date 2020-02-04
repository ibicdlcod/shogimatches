from bracketgen import title_match
from importdata import sql_read
from metastruct import organized_tr


def shidan_title_matches(iteration_int: int):
    iteration_str = f"第{str(iteration_int).zfill(2)}期"
    iteration_str_prev = f"第{str(iteration_int - 1).zfill(2)}期"
    # 七番勝負
    title_matches = sql_read.read_match("十段戦", iteration_str, "タイトル戦", "七番勝負")
    if iteration_int != 1:
        title_matches_last = sql_read.read_match("十段戦", iteration_str_prev, "タイトル戦", "七番勝負")
        org_tree_title_last = organized_tr.OrganizedTree(title_matches_last, f"タイトル戦七番勝負", ["", ])
    else:
        org_tree_title_last = None
    org_tree_title = organized_tr.OrganizedTree(title_matches, f"タイトル戦七番勝負", ["", ])
    return title_match.title_match_str(org_tree_title,
                                       "十段戦",
                                       iteration_str,
                                       "十段",
                                       "七番勝負",
                                       org_tree_title_last)
