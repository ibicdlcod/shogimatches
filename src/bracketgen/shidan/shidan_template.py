from bracketgen.shidan import shidan_2_3, shidan_4, shidan_5_15, shidan_16_26, kudan


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
               "[[Category:十段戦関連のテンプレート]]\n"
               "</noinclude>\n")
    return result


def order(in_str):
    if in_str == "INFOBOX":
        return 0
    elif in_str == "LEAD":
        return 1
    elif in_str == 9:
        return 5
    elif in_str == 7:
        return 7
    elif in_str == 0:
        return 10
    elif in_str == "REMAIN_W":
        return 11
    elif in_str == "SUBST_W":
        return 12
    elif in_str == 3:
        return 17
    elif in_str == 2:
        return 18
    elif in_str == 1:
        return 19
    else:
        return 99


def gen_usage(iteration: str, in_str_dict_keys: list):
    result = "<!-- Please report bugs to https://github.com/ibicdlcod/shogimatches/issues -->\n"
    in_str_dict_keys.sort(key=order)
    iteration_int = int(iteration.lstrip("第").rstrip("期"))
    for key in in_str_dict_keys:
        if key == 0:
            result += f"=={iteration}十段戦挑戦者決定リーグ戦==\n"
        elif key == 1:
            result += "==一次予選==\n"
        elif key == 2:
            result += "==二次予選==\n"
        elif key == 3:
            result += "==三次予選==\n"
        elif key == 4:
            result += "==予選==\n"
        elif key == "REMAIN_W":
            result += "===残留決定戦===\n"
        elif key == "SUBST_W":
            result += "===補欠決定戦===\n"
        result += "{{" + iteration + "十段戦|group=" + str(key) + "}}\n"
    result += (
        "== 出典 ==\n"
        f"*[http://shogititle.nobody.jp/table/ryuo/judan-{str(iteration_int).zfill(2)}.html "
        f"第{iteration_int}期十段戦：将棋タイトル戦]\n"
        "{{各期の十段戦}}\n"
        "{{Shogi-stub}}\n"
        "{{" + f"DEFAULTSORT:しゆうたんせん{str(iteration_int).zfill(2)}き" + "}}\n"
        f"[[Category:竜王戦|{1960+iteration_int}-{61+iteration_int}]]\n"
        f"[[Category:{1960+iteration_int}年の日本]]\n"
        f"[[Category:{1961+iteration_int}年の日本]]\n"
    )
    return result


def gen_usage_kudan(iteration: str, in_str_dict_keys: list):
    result = "<!-- Please report bugs to https://github.com/ibicdlcod/shogimatches/issues -->\n"
    in_str_dict_keys.sort(key=order)
    iteration_int = int(iteration.lstrip("第").rstrip("期"))
    for key in in_str_dict_keys:
        if key == 0:
            result += f"==本戦==\n"
        elif key == 1:
            result += "==一次予選==\n"
        elif key == 2:
            result += "==二次予選==\n"
        elif key == 3:
            result += "==三次予選==\n"
        elif key == 4:
            result += "==予選==\n"
        result += "{{" + iteration + "九段戦|group=" + str(key) + "}}\n"
    result += (
        "== 出典 ==\n"
        f"*[http://shogititle.nobody.jp/table/ryuo/kudan-{str(iteration_int).zfill(2)}.html "
        f"第{iteration_int}期九段戦：将棋タイトル戦]\n"
        "{{各期の九段戦}}\n"
        "{{Shogi-stub}}\n"
        "{{" + f"DEFAULTSORT:九段戦{str(iteration_int).zfill(2)}き" + "}}\n"
        f"[[Category:竜王戦|{1948+iteration_int}-{49+iteration_int}]]\n"
        f"[[Category:{1948+iteration_int}年の日本]]\n"
        f"[[Category:{1949+iteration_int}年の日本]]\n"
    )
    return result


def shidan_str(i: int):
    if i >= 16:
        dict_result = shidan_16_26.shidan_str_dict(i)
    elif (16 > i >= 5) or (i == 1):
        dict_result = shidan_5_15.shidan_str_dict(i)
    elif i == 4:
        dict_result = shidan_4.shidan_str_dict(i)
    else:
        dict_result = shidan_2_3.shidan_str_dict(i)

    return gen_template(dict_result), gen_usage(f"第{str(i).zfill(2)}期", list(dict_result.keys()))


def kudan_str(i: int):
    dict_result = kudan.kudan_str_dict(i)

    return gen_template(dict_result), gen_usage_kudan(f"第{str(i).zfill(2)}期", list(dict_result.keys()))