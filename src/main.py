from bracketgen.ouza import ouza_template
from importdata import birthday, kishi_all, match_mass
import gen_config
import gen_content
import re

if __name__ == '__main__':
    gen_conf = gen_config.read_primary_config()
    update_on = (gen_conf["read_update_on"] == "True")
    birthday_on = (gen_conf["birthday_on"] == "True")

    if update_on:
        kishi_db = kishi_all.gen_kishi_db()
        if birthday_on:
            birthday.gen_birthday(kishi_db)

        outfile_name = "txt_src\\names2.csv"
        outfile = open(outfile_name, 'w', encoding="utf-8-sig")
        for i in kishi_db:
            outfile.write(str(i) + "\n")
        outfile.close()

    match_mass.match_mass()

    gen_content.content()

    # infile_name = f"oui.txt"
    # infile = open(infile_name, "r", encoding="utf-8-sig")
    # outfile_name = f"oui_out.txt"
    # outfile = open(outfile_name, "w", encoding="utf-8-sig")
    # re_pattern = re.compile(r"^!(\d*)$")
    # line = infile.readline()
    # while line:
    #     # print(line)
    #     re_match = re.match(re_pattern, line)
    #     if re_match is not None:
    #         outfile.write(re.sub(re_pattern, r"![[第\1期王位戦|\1]]", line))
    #     else:
    #         outfile.write(line)
    #     line = infile.readline()
    # infile.close()
    # outfile.close()
