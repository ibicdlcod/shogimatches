from bracketgen.ouza import ouza_main


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
               "[[Category:王座戦関連のテンプレート]]\n"
               "</noinclude>\n")
    return result


def order(in_str):
    if in_str == "INFOBOX":
        return 0
    elif in_str == "LEAD":
        return 1
    elif in_str == "T":
        return 7
    elif in_str == 0:
        return 10
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
        if key == "PLAYOFFS":
            result += f"==リーグプレーオフ==\n"
        elif key == 0:
            result += ("==本戦==\n" if iteration_int < 18 else "==挑戦者決定トーナメント==\n")
        elif key == 2:
            result += ("==二次予選==\n" if iteration_int >= 4 else "==予選==\n")
        elif key == 1:
            result += "==一次予選==\n"
        result += in_str_dict[key]
    year_at = str(52 + iteration_int)
    if iteration_int == 48:
        year_at = str(2000)
    elif iteration_int > 48:
        year_at = str(iteration_int - 48).zfill(2)
    kenyu_int = (1000 + iteration_int) if iteration_int >= 31 else (2000 + iteration_int)
    q_or_h = "期" if iteration_int >= 31 else "回"
    result += (
        "== 出典 ==\n"
        f"*[https://www.shogi.or.jp/match/ouza/ 王座戦：日本将棋連盟]\n"
        f"*[https://www.shogi.or.jp/publish/shogi_nenkan.html 将棋年鑑]\n"
        f"*[http://kenyu1234.php.xdomain.jp/resultsm.php?sen=0&pd={kenyu_int}&mn=5 "
        f"第{iteration_int}{q_or_h}王座戦：将棋棋士成績DB]\n"
        f"*[http://shogititle.nobody.jp/table/ouza/ouza-{str(iteration_int).zfill(2)}.html "
        f"第{iteration_int}{q_or_h}王座戦：将棋タイトル戦]\n"
        "{{各期の王座戦}}\n"
        "{{Shogi-stub}}\n"
        "{{" + f"DEFAULTSORT:王座戦{str(iteration_int).zfill(2)}き" + "}}\n"
        f"[[Category:王座戦 (将棋)|{1951+iteration_int}-{year_at}]]\n"
        f"[[Category:{1951+iteration_int}年の日本]]\n"
        f"[[Category:{1952+iteration_int}年の日本]]\n"
    )
    return result


def ouza_str(iteration_int: int):
    dict_result = ouza_main.ouza_str_dict(iteration_int)

    iteration_str = (f"第{str(iteration_int).zfill(2)}期"
                     if iteration_int >= 31
                     else f"第{str(iteration_int).zfill(2)}回")

    return gen_template(dict_result), gen_usage(f"{iteration_str}", dict_result)

