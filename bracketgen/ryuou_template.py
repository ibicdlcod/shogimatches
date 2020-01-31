def gen_template(in_str_dict: dict):
    result = "{{#switch:{{lc:{{{group}}}}}|"
    for k, v in in_str_dict.items():
        v2 = v.replace("|", "{{!}}")
        result += f"|{k}={v2}"
    result += "|}}\n"
    result += ("<noinclude>\n"
               "[[Category:竜王戦|各]]\n"
               "[[Category:トーナメントに関するテンプレート|竜]]\n"
               "[[Category:将棋関連のテンプレート|竜]]\n"
               "</noinclude>\n")
    return result


def gen_usage(iteration: str, in_str_dict_keys):
    result = "<!-- Please report bugs to https://github.com/ibicdlcod/shogimatches/issues -->\n"
    for key in in_str_dict_keys:
        result += "{{" + iteration + "竜王戦|group=" + str(key) + "}}\n"
    return result
