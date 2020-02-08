from bracketgen.oui import oui_main


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
               "[[Category:王位戦関連のテンプレート]]\n"
               "</noinclude>\n")
    return result


def order(in_str):
    if in_str == "INFOBOX":
        return 0
    elif in_str == "LEAD":
        return 1
    elif in_str == "T":
        return 7
    elif in_str == "PLAYOFFS":
        return 8
    elif in_str == "RED":
        return 11
    elif in_str == "WHITE":
        return 12
    elif in_str == "REMAINS":
        return 19
    elif in_str == "PRELIMINARY":
        return 40
    else:
        return 99


def gen_usage(iteration: str, in_str_dict: dict):
    result = "<!-- Please report bugs to https://github.com/ibicdlcod/shogimatches/issues -->\n"
    in_str_dict_keys = list(in_str_dict.keys())
    in_str_dict_keys.sort(key=order)
    iteration_int = int(iteration.lstrip("第").rstrip("期").rstrip("回"))
    for key in in_str_dict_keys:
        if key == "PLAYOFFS":
            result += f"==リーグプレーオフ==\n"
        elif key == "RED":
            result += ("==紅組==\n" if iteration_int >= 3 else "==A組==\n")
        elif key == "WHITE":
            result += ("==白組==\n" if iteration_int >= 3 else "==B組==\n")
        elif key == "REMAINS":
            result += f"==残留プレーオフ==\n"
        elif key == "PRELIMINARY":
            result += "==予選==\n"
        result += in_str_dict[key]
    year_at = str(59 + iteration_int)
    if iteration_int == 41:
        year_at = str(2000)
    elif iteration_int > 41:
        year_at = str(iteration_int - 41).zfill(2)
    kenyu_int = 1000 + iteration_int
    result += (
        "== 出典 ==\n"
        f"*[https://www.shogi.or.jp/match/oui/ 王位戦：日本将棋連盟]\n"
        f"*[https://www.shogi.or.jp/publish/shogi_nenkan.html 将棋年鑑]\n"
        f"*[http://kenyu1234.php.xdomain.jp/resultsm.php?sen=0&pd={kenyu_int}&mn=4 "
        f"第{iteration_int}期王位戦：将棋棋士成績DB]\n"
        f"*[http://shogititle.nobody.jp/table/oui/oui-{str(iteration_int).zfill(2)}.html "
        f"第{iteration_int}期王位戦：将棋タイトル戦]\n"
        "{{各期の王位戦}}\n"
        "{{Shogi-stub}}\n"
        "{{" + f"DEFAULTSORT:王位戦{str(iteration_int).zfill(2)}き" + "}}\n"
        f"[[Category:王位戦|{1958+iteration_int}-{year_at}]]\n"
        f"[[Category:{1958+iteration_int}年の日本]]\n"
        f"[[Category:{1959+iteration_int}年の日本]]\n"
    )
    return result


def oui_str(i: int):
    dict_result = oui_main.oui_str_dict(i)
    return gen_template(dict_result), gen_usage(f"第{str(i).zfill(2)}期", dict_result)

