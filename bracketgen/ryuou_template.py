def gen_template(in_str_dict: dict):
    result = "{{#switch:{{lc:{{{group}}}}}|"
    for k, v in in_str_dict.items():
        v2 = v.replace("|", "{{!}}")
        result += f"|{k}={v2}"
    result += "|}}"
    return result
