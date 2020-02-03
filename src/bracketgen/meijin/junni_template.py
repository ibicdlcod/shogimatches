def gen_template(in_str_dict: dict):
    result = "<noinclude>{{複雑なテンプレート}}</noinclude>{{#switch:{{{group}}}"
    for k, v in in_str_dict.items():
        v2 = v.replace("|", "{{!}}")
        v3 = v2.replace("colorbox{{!}}", "colorbox|")
        result += f"|{k}={v3}"
    result += "|}}\n"
    result += ("<noinclude>\n"
               "[[Category:順位戦関連のテンプレート]]\n"
               "</noinclude>\n")
    return result


def order(in_str: str):
    if in_str == "M":
        return 0
    elif in_str == "HEAD":
        return 1
    elif in_str == "AP":
        return 9
    elif in_str == "A":
        return 10
    elif in_str == "B1":
        return 21
    elif in_str == "B2":
        return 22
    elif in_str == "C1":
        return 31
    elif in_str == "C2":
        return 32
    elif in_str == "FC":
        return 60
    else:
        return 99


def gen_usage(iteration: str, in_str_dict_keys: list):
    result = "<!-- Please report bugs to https://github.com/ibicdlcod/shogimatches/issues -->\n"
    in_str_dict_keys.sort(key=order)
    for key in in_str_dict_keys:
        if key == "A":
            result += "===A級===\n"
        if key == "AP":
            result += "===A級プレーオフ===\n"
        elif key == "B1":
            result += "===B級1組===\n"
        elif key == "B2":
            result += "===B級2組===\n"
        elif key == "C1":
            result += "===C級1組===\n"
        elif key == "C2":
            result += "===C級2組===\n"
        elif key == "FC":
            result += "===フリークラス===\n"
        elif key == "HEAD":
            result += "==順位戦==\n"
        result += "{{" + iteration + "順位戦|group=" + str(key) + "}}\n"
    return result
