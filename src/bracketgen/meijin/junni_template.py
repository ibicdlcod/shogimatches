import re


def gen_template(in_str_dict: dict):
    result = "<noinclude>{{複雑なテンプレート}}</noinclude>{{#switch:{{{group}}}"
    for k, v in in_str_dict.items():
        v2 = v.replace("|", "{{!}}")
        v3 = v2.replace("colorbox{{!}}", "colorbox|")
        v4 = re.sub(r'{{Sort{{!\}\}(.*?){{!\}\}(.*?)\}\}',
                    r"{{Sort|\1|\2}}",
                    v3)
        result += f"|{k}={v4}"
    result += "|}}\n"
    result += ("<noinclude>\n"
               "[[Category:順位戦関連のテンプレート]]\n"
               "</noinclude>\n")
    return result
# re.sub(r'\{\{Sort\{\{!\}\}(.*)\{\{!\}\}(.*)\}\}',
# ...        r"{{Sort|\1|\2}}",
# ...        r'{{Sort{{!}}58{{!}}八段}}')


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
    iteration_int = int(iteration.lstrip("第").rstrip("期"))
    for key in in_str_dict_keys:
        if key == "A":
            if 36 <= iteration_int < 44:
                result += "===名人戦挑戦者決定リーグ戦===\n"
            else:
                result += "===A級===\n"
        if key == "AP":
            if 36 <= iteration_int < 44:
                result += "===名人戦挑戦者決定プレーオフ===\n"
            else:
                result += "===A級プレーオフ===\n"
        elif key == "B1":
            if 36 <= iteration_int < 44:
                result += "===昇降級リーグ戦1組===\n"
            else:
                result += "===B級1組===\n"
        elif key == "B2":
            if 36 <= iteration_int < 44:
                result += "===昇降級リーグ戦2組===\n"
            else:
                result += "===B級2組===\n"
        elif key == "C1":
            if 36 <= iteration_int < 44:
                result += "===昇降級リーグ戦3組===\n"
            else:
                result += "===C級1組===\n"
        elif key == "C2":
            if 36 <= iteration_int < 44:
                result += "===昇降級リーグ戦4組===\n"
            else:
                result += "===C級2組===\n"
        elif key == "FC":
            result += "===フリークラス===\n"
        elif key == "HEAD":
            result += "==順位戦==\n"
        result += "{{" + iteration + "順位戦|group=" + str(key) + "}}\n"
    return result
