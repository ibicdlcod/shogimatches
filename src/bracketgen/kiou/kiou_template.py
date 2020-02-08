from bracketgen.kiou import kiou_main


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
               "[[Category:棋王戦関連のテンプレート]]\n"
               "</noinclude>\n")
    return result


def order(in_str):
    if in_str == "INFOBOX":
        return 0
    elif in_str == "LEAD":
        return 1
    elif in_str == "T":
        return 7
    elif in_str == "TP":
        return 8
    elif in_str == "DECISIVE":
        return 9
    elif in_str == "WINNERS":
        return 10
    elif in_str == "LOSERS":
        return 11
    elif in_str == "PRELIMINARY":
        return 20
    else:
        return 99


def gen_usage(iteration: str, in_str_dict: dict):
    result = "<!-- Please report bugs to https://github.com/ibicdlcod/shogimatches/issues -->\n"
    in_str_dict_keys = list(in_str_dict.keys())
    in_str_dict_keys.sort(key=order)
    iteration_int = int(iteration.lstrip("第").rstrip("期").rstrip("回"))
    for key in in_str_dict_keys:
        if key == "TP":
            result += f"==第01期棋王戦決勝リーグ戦==\n"
        elif key == "WINNERS":
            result += "==挑戦者決定トーナメント==\n===勝者組===\n"
        elif key == "LOSERS":
            result += "===敗者復活戦===\n"
        elif key == "PRELIMINARY":
            result += "==予選==\n"
        result += in_str_dict[key]
    year_at = str(75 + iteration_int)
    if iteration_int == 25:
        year_at = str(2000)
    elif iteration_int > 25:
        year_at = str(iteration_int - 25).zfill(2)
    kenyu_int = (1000 + iteration_int)
    q_or_h = "期" if iteration_int != 1001 else "回"
    result += (
        "== 出典 ==\n"
        f"*[https://www.shogi.or.jp/match/kiou/ 棋王戦：日本将棋連盟]\n"
        f"*[https://www.shogi.or.jp/publish/shogi_nenkan.html 将棋年鑑]\n"
        f"*[http://kenyu1234.php.xdomain.jp/resultsm.php?sen=0&pd={kenyu_int}&mn=6 "
        f"第{iteration_int}{q_or_h}棋王戦：将棋棋士成績DB]\n"
        f"*[http://shogititle.nobody.jp/table/kiou/kiou-{str(iteration_int).zfill(2)}.html "
        f"第{iteration_int}{q_or_h}棋王戦：将棋タイトル戦]\n"
        "{{各期の棋王戦}}\n"
        "{{Shogi-stub}}\n"
        "{{" + f"DEFAULTSORT:棋王戦{str(iteration_int).zfill(2)}き" + "}}\n"
        f"[[Category:棋王戦 (将棋)|{1974+iteration_int}-{year_at}]]\n"
        f"[[Category:{1974+iteration_int}年の日本]]\n"
        f"[[Category:{1975+iteration_int}年の日本]]\n"
    )
    return result


def kiou_str(iteration_int: int):
    dict_result = kiou_main.kiou_str_dict(iteration_int)

    iteration_str = (f"第{str(iteration_int).zfill(2)}期"
                     if iteration_int != 1001
                     else f"第{str(iteration_int - 1000).zfill(2)}回")

    return gen_template(dict_result), gen_usage(f"{iteration_str}", dict_result)

