from bracketgen.kisei import kisei_main


def gen_template(in_str_dict: dict):
    result = "<noinclude>{{複雑なテンプレート}}</noinclude>{{#switch:{{{group}}}"
    for k, v in in_str_dict.items():
        if k != "INFOBOX":
            v2 = v.replace("|", "{{!}}")
        else:
            v2 = v
        result += f"|{k}={v2}"
    result += "|}}\n"
    result += ("<noinclude>\n"
               "[[Category:棋聖戦関連のテンプレート]]\n"
               "</noinclude>\n")
    return result


def order(in_str):
    if in_str == "INFOBOX":
        return 0
    elif in_str == "LEAD":
        return 1
    elif in_str == "T":
        return 7
    elif in_str == "TG":
        return 8
    elif in_str == 0:
        return 10
    elif in_str == 9 or in_str == 3:
        return 17
    elif in_str == 2:
        return 18
    elif in_str == 1:
        return 19
    else:
        return 99


def gen_usage(iteration: str, in_str_dict: dict):
    result = "<!-- Please report bugs to https://github.com/ibicdlcod/shogimatches/issues -->\n"
    in_str_dict_keys = list(in_str_dict.keys())
    in_str_dict_keys.sort(key=order)
    iteration_int = int(iteration.lstrip("第").rstrip("期").rstrip("回"))
    for key in in_str_dict_keys:
        if key == "TG":
            result += f"==第１期（1962年度後期）棋聖戦三者リーグ==\n"
        elif key == 0:
            result += ("==本戦==\n" if iteration_int < 66 else "==決勝トーナメント==\n")
        elif key == 9:
            result += "==最終予選==\n"
        elif key == 3:
            result += "==三次予選==\n"
        elif key == 2:
            result += "==二次予選==\n"
        elif key == 1:
            result += "==一次予選==\n"
        result += in_str_dict[key]

    if iteration_int < 66:
        year_held = (iteration_int // 2) + 1962
        if (iteration_int % 2) == 0:
            year_from = year_held
        else:
            year_from = year_held
            year_held = year_held + 1
    else:
        year_held = 1929 + iteration_int
        year_from = year_held - 1

    if year_held == year_from:
        from_to_end_str = str(year_held)
    else:
        end_str = str(year_held)
        if end_str == "2000":
            pass
        elif end_str.startswith("19"):
            end_str = end_str[2:]
        elif end_str.startswith("20"):
            end_str = end_str[2:]
        from_to_end_str = f"{year_from}-{end_str}"

    kenyu_int = 1000 + iteration_int
    result += (
        "== 出典 ==\n"
        f"*[https://www.shogi.or.jp/match/kisei/ 棋聖戦：日本将棋連盟]\n"
        f"*[https://www.shogi.or.jp/publish/shogi_nenkan.html 将棋年鑑]\n"
        "{{各期の棋聖戦 (将棋)}}\n"
        "{{Shogi-stub}}\n"
        "{{" + f"DEFAULTSORT:棋聖戦{str(iteration_int).zfill(2)}き" + "}}\n"
        f"[[Category:棋聖戦 (将棋)|{from_to_end_str}]]\n"
        + (f"[[Category:{year_from}年の日本]]\n" if year_held != year_from else "")
        + f"[[Category:{year_held}年の日本]]\n"
    )
    return result


def kisei_str(iteration_int: int):
    dict_result = kisei_main.kisei_str_dict(iteration_int)

    iteration_str = f"第{str(iteration_int).zfill(2)}期"

    return gen_template(dict_result), gen_usage(f"{iteration_str}", dict_result)
