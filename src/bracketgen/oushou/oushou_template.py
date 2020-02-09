from bracketgen.oushou import oushou_main


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
               "[[Category:王将戦関連のテンプレート]]\n"
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
        return 9
    elif in_str == 0:
        return 10
    elif in_str == "REMAINS":
        return 11
    elif in_str == 2:
        return 18
    elif in_str == 1:
        return 19
    else:
        return 99


def gen_usage(iteration: str, in_str_dict: dict):
    in_str_dict_keys = list(in_str_dict.keys())
    result = "<!-- Please report bugs to https://github.com/ibicdlcod/shogimatches/issues -->\n"
    in_str_dict_keys.sort(key=order)
    iteration_int = int(iteration.lstrip("第").rstrip("期"))
    for key in in_str_dict_keys:
        if key == "PLAYOFFS":
            result += f"==挑戦者決定プレーオフ==\n"
        elif key == 0:
            result += f"==挑戦者決定リーグ==\n"
        elif key == "REMAINS":
            result += f"==残留決定戦==\n"
        elif key == 1:
            result += "==一次予選==\n"
        elif key == 2:
            result += "==二次予選==\n"
        # result += "{{" + iteration + "王将戦|group=" + str(key) + "}}\n"
        result += in_str_dict[key] + "\n"
    kenyu_int = 1000 + iteration_int
    result += (
        "== 出典 ==\n"
        f"*[https://www.shogi.or.jp/match/oushou/ 王将戦：日本将棋連盟]\n"
        f"*[https://www.shogi.or.jp/publish/shogi_nenkan.html 将棋年鑑]\n"
        f"*[http://kenyu1234.php.xdomain.jp/resultsm.php?sen=0&pd={kenyu_int}&mn=7 "
        f"第{iteration_int}期王将戦：将棋棋士成績DB]\n"
        f"*[http://shogititle.nobody.jp/table/oushou/oushou-{str(iteration_int).zfill(2)}.html "
        f"第{iteration_int}期王将戦：将棋タイトル戦]\n"
        "{{各期の王将戦}}\n"
        "{{Shogi-stub}}\n"
        "{{" + f"DEFAULTSORT:王将戦{str(iteration_int).zfill(2)}き" + "}}\n"
        f"[[Category:王将戦|{1950+iteration_int}-{51+iteration_int}]]\n"
        f"[[Category:{1950+iteration_int}年の日本]]\n"
        f"[[Category:{1951+iteration_int}年の日本]]\n"
    )
    return result


def oushou_str(i: int):
    dict_result = oushou_main.oushou_str_dict(i)

    return gen_template(dict_result), gen_usage(f"第{str(i).zfill(2)}期", dict_result)