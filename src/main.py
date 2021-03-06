import gen_config
import gen_content
import re
from importdata import birthday, kishi_all, match_mass

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

    # infile_name = f"kisei.txt"
    # infile = open(infile_name, "r", encoding="utf-8-sig")
    # outfile_name = f"kisei_out.txt"
    # outfile = open(outfile_name, "w", encoding="utf-8-sig")
    # re_pattern = re.compile(r"^!(\d*)$")
    # line = infile.readline()
    # while line:
    #     re_match = re.match(re_pattern, line)
    #     if re_match is not None:
    #         outfile.write(re.sub(re_pattern, r"![[第\1期棋聖戦 (将棋)|\1]]", line))
    #     else:
    #         outfile.write(line)
    #     line = infile.readline()
    # infile.close()
    # outfile.close()

    # outfile_name = f"temp.txt"
    # outfile = open(outfile_name, "w", encoding="utf-8-sig")
    # outfile.write(
    #     "{{Navbox\n"
    #     "| name = 各期の棋聖戦\n"
    #     "| title = 各期の[[棋聖戦 (将棋)|棋聖戦]]\n"
    #     "| listclass = hlist hlist - pipe hnum\n"
    #     "| titlestyle = background - color:  # CCCCFF; color:#000\n"
    #     "| groupstyle = background - color:  # CCCCFF; text-align:center\n"
    # )
    # for i in range(10):
    #     outfile.write(f"|list{i+1}=")
    #     for j in range(10):
    #         this_num = i * 10 + j + 1
    #         iteration_end = "期"
    #
    #         first_or_second_half = ""
    #         if this_num < 66:
    #             if (this_num % 2) == 0:
    #                 first_or_second_half = "前"
    #             else:
    #                 first_or_second_half = "後"
    #         if this_num < 66:
    #             year_held = (this_num // 2) + 1962
    #         else:
    #             year_held = 1929 + this_num
    #
    #         outfile.write(f"[[第{this_num}{iteration_end}棋聖戦 (将棋)|{str(this_num).zfill(2)}"
    #                       f"({year_held}{first_or_second_half})]]")
    #         if j != 9:
    #             outfile.write(" - ")
    #     outfile.write("\n")
    # outfile.write(
    #     "}}<noinclude>\n"
    #     "[[Category:棋聖戦 (将棋)|*]]\n"
    #     "[[Category: 将棋関連のテンプレート]] </noinclude>\n"
    # )
    # outfile.close()

    # outfile_name = f"temp.txt"
    # outfile = open(outfile_name, "w", encoding="utf-8-sig")
    # outfile.write(
    #     "{{Navbox\n"
    #     "| name = 各期の王座戦 (将棋)\n"
    #     "| title = 各期の[[王座戦 (将棋)|王座戦]]\n"
    #     "| listclass = hlist hlist - pipe hnum\n"
    #     "| titlestyle = background - color:  # CCCCFF; color:#000\n"
    #     "| groupstyle = background - color:  # CCCCFF; text-align:center\n"
    # )
    # for i in range(7):
    #     outfile.write(f"|list{i+1}=")
    #     for j in range(10):
    #         this_num = i * 10 + j + 1
    #         iteration_end = "期" if this_num > 30 else "回"
    #         outfile.write(f"[[第{this_num}{iteration_end}王座戦 (将棋)|{str(this_num).zfill(2)}({1959+this_num})]]")
    #         if j != 9:
    #             outfile.write(" - ")
    #     outfile.write("\n")
    # outfile.write(
    #     "}}<noinclude>\n"
    #     "[[Category:王座戦 (将棋)|*]]\n"
    #     "[[Category: 将棋関連のテンプレート]] </noinclude>\n"
    # )
    # outfile.close()

    # infile_name = f"ouza.txt"
    # infile = open(infile_name, "r", encoding="utf-8-sig")
    # outfile_name = f"ouza_out.txt"
    # outfile = open(outfile_name, "w", encoding="utf-8-sig")
    # re_pattern = re.compile(r"^!\[\[第(\d+?)([期回])王座戦\|(\1)\]\]$")
    # line = infile.readline()
    # while line:
    #     re_match = re.match(re_pattern, line)
    #     if re_match is not None and re_match.group(1):
    #         outfile.write(re.sub(re_pattern, r"![[第\1\2王座戦 (将棋)|\1]]", line))
    #         print(re_match.group(1))
    #     else:
    #         outfile.write(line)
    #     line = infile.readline()
    # infile.close()
    # outfile.close()
