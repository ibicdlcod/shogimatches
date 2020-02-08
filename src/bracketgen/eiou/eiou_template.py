from bracketgen.eiou import eiou_new, eiou_old


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
               "[[Category:叡王戦関連のテンプレート]]\n"
               "</noinclude>\n")
    return result


def order(in_str):
    if in_str == "INFOBOX":
        return 0
    elif in_str == "LEAD":
        return 1
    elif in_str == "T":
        return 7
    elif int(in_str) != 0 and 4 <= in_str <= 9:
        return 20 - in_str
    elif in_str == 0:
        return 10
    else:
        return 99


def gen_usage(iteration: str, in_str_dict: dict):
    in_str_dict_keys = list(in_str_dict.keys())
    result = "<!-- Please report bugs to https://github.com/ibicdlcod/shogimatches/issues -->\n"
    in_str_dict_keys.sort(key=order)
    iteration_int = int(iteration.lstrip("第").rstrip("期").rstrip("回"))
    for key in in_str_dict_keys:
        if key == 0:
            result += f"=={iteration}叡王戦本戦==\n"
        elif key == 9:
            result += "==九段戦==\n"
        elif key == 8:
            result += "==八段戦==\n"
        elif key == 7:
            result += "==七段戦==\n"
        elif key == 6:
            result += "==六段戦==\n"
        elif key == 5:
            result += "==五段戦==\n"
        elif key == 4:
            result += "==四段戦==\n"
        result += in_str_dict[key] + "\n"
        # result += "{{" + iteration + "叡王戦|group=" + str(key) + "}}\n"
    kenyu_int = (1000 + iteration_int) if iteration_int >= 3 else (2000 + iteration_int)
    result += (
        "== 出典 ==\n"
        f"*[https://www.shogi.or.jp/match/eiou/ 叡王戦：日本将棋連盟]\n"
        f"*[https://www.shogi.or.jp/publish/shogi_nenkan.html 将棋年鑑]\n"
        f"*[http://kenyu1234.php.xdomain.jp/resultsm.php?sen=0&pd={kenyu_int}&mn=12 "
        f"{iteration}叡王戦：将棋棋士成績DB]\n"
        f"*[http://shogititle.nobody.jp/table/eiou/eiou-{str(iteration_int).zfill(2)}.html "
        f"{iteration}叡王戦：将棋タイトル戦]\n"
        "{{各期の叡王戦}}\n"
        "{{Shogi-stub}}\n"
        "{{" + f"DEFAULTSORT:叡王戦{str(iteration_int).zfill(2)}き" + "}}\n"
        f"[[Category:叡王戦|{2014+iteration_int}]]\n"
        f"[[Category:{2014+iteration_int}年の日本]]\n"
    )
    return result


def eiou_str(i: int):
    if i <= 2:
        dict_result = eiou_old.eiou_str_dict(i)
        return gen_template(dict_result), gen_usage(f"第{str(i).zfill(2)}回", dict_result)
    else:
        dict_result = eiou_new.eiou_str_dict(i)
        return gen_template(dict_result), gen_usage(f"第{str(i).zfill(2)}期", dict_result)

