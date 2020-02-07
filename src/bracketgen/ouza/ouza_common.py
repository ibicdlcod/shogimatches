from bracketgen import title_match
from importdata import sql_read
from metastruct import organized_tr


def ouza_title_matches(iteration_int: int):
    iteration_str = f"第{str(iteration_int).zfill(2)}期"
    iteration_str_prev = (f"第{str(iteration_int - 1).zfill(2)}期"
                          if iteration_int != 31
                          else "第30回")
    # 五番勝負
    title_length_str = "五番勝負" if iteration_int != 31 else "三番勝負"
    title_length_str_prev = "五番勝負" if iteration_int != 32 else "三番勝負"
    title_matches = sql_read.read_match("王座戦", iteration_str, "タイトル戦", title_length_str)
    if iteration_int == 31:
        title_matches_last = sql_read.read_match("王座戦", iteration_str_prev, "準タイトル戦", "三番勝負")
        org_tree_title_last = organized_tr.OrganizedTree(title_matches_last, f"準タイトル戦三番勝負", ["", ])
    else:
        title_matches_last = sql_read.read_match("王座戦", iteration_str_prev, "タイトル戦", title_length_str_prev)
        org_tree_title_last = organized_tr.OrganizedTree(title_matches_last, f"タイトル戦" + title_length_str_prev,
                                                         ["", ])
    org_tree_title = organized_tr.OrganizedTree(title_matches, f"タイトル戦" + title_length_str, ["", ])
    return title_match.title_match_str_plus(org_tree_title,
                                            "王座戦",
                                            iteration_str,
                                            "王座",
                                            "五番勝負",
                                            org_tree_title_last)


def ouza_pseudo_title_matches(iteration_int: int):
    iteration_str = f"第{str(iteration_int).zfill(2)}回"
    iteration_str_prev = (f"第{str(iteration_int - 1).zfill(2)}回"
                          if iteration_int != 1
                          else "")
    # 三番勝負
    title_matches = sql_read.read_match("王座戦", iteration_str, "準タイトル戦", "三番勝負")
    if iteration_int <= 18:
        org_tree_title_last = None
    else:
        title_matches_last = sql_read.read_match("王座戦", iteration_str_prev, "準タイトル戦", "三番勝負")
        org_tree_title_last = organized_tr.OrganizedTree(title_matches_last, f"準タイトル戦三番勝負", ["", ])
    org_tree_title = organized_tr.OrganizedTree(title_matches, f"準タイトル戦三番勝負", ["", ])
    return title_match.title_match_str_plus(org_tree_title,
                                            "王座戦",
                                            iteration_str,
                                            "王座",
                                            "三番勝負",
                                            org_tree_title_last)
