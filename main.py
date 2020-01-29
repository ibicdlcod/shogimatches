import importdata.kishi_txt as txt
from metastruct import organized_t
from bracketgen import bra_from_tr
from importdata import sql_read, gen_round_name

if __name__ == '__main__':
    kishi_db = []
    update_on = False
    if update_on:
        kishi_db = txt.process_txt()
        amateur1 = txt.process_more_txt("current_amateur_part")
        amateur_w = txt.process_more_txt("current_amateur_woman")
        former_srk = txt.process_more_txt("former_shoreikai")
        current_3dan = txt.process_more_txt("sandan")
        women = txt.process_more_txt("woman")

        for kishi in kishi_db:
            i = kishi.id
            if i in amateur1 or i in amateur_w or i in former_srk:
                kishi.current_amateur = True
            if i in amateur_w or i in women or kishi.fullname == "西山朋佳":
                """
                Special treatment, eh?
                Note her name blatantly occurs in password of this project
                (root was not used so as not to compromise my own MySQL password)
                note male shoreikai members <= 2dan does not appear in matches.
                Aside from female shoreikai members gone to female professional,
                中七海 and 今井絢 is still treated as amateurs by http://kenyu1234.php.xdomain.jp/
                """
                kishi.woman = True
            if i in current_3dan:
                kishi.current_shoreikai = True

        kishi_db = txt.sql_connect(False, True, kishi_db)

        outfile_name = "..\\txt_src\\names2.csv"
        outfile = open(outfile_name, 'w', encoding="utf-8-sig")
        for i in kishi_db:
            outfile.write(str(i) + "\n")
        outfile.close()
    outfile_name = "temp.txt"
    outfile = open(outfile_name, 'w', encoding="utf-8-sig")

    match_db2 = sql_read.read_match("竜王戦", "第01期", "決勝トーナメント")
    round_db2 = gen_round_name.read_round("竜王戦", "第01期", "決勝トーナメント")
    org_tree2 = organized_t.OrganizedTree(match_db2, "決勝トーナメント", round_db2)
    table_2 = bra_from_tr.generate_bra_pos(org_tree2, dict(), dict(), True, True)
    draw_table_2 = bra_from_tr.draw_table(table_2, "竜王戦第01期" + org_tree2.display_name)
    outfile.write(draw_table_2)

    match_db2 = sql_read.read_match("竜王戦", "第01期", "1組", "ランキング戦")
    round_db2 = gen_round_name.read_round("竜王戦", "第01期", "1組", "ランキング戦")
    print(round_db2)
    org_tree2 = organized_t.OrganizedTree(match_db2, "1組ランキング戦", round_db2)
    table_2 = bra_from_tr.generate_bra_pos(org_tree2, dict(), dict(), False, True)
    draw_table_2 = bra_from_tr.draw_table(table_2, "竜王戦第01期" + org_tree2.display_name)
    outfile.write(draw_table_2)

    match_db2 = sql_read.read_match("竜王戦", "第01期", "1組", "3位出場者決定戦")
    round_db2 = gen_round_name.read_round("竜王戦", "第01期", "1組", "3位出場者決定戦")
    print(round_db2)
    org_tree2 = organized_t.OrganizedTree(match_db2, "1組3位出場者決定戦", round_db2)
    table_2 = bra_from_tr.generate_bra_pos(org_tree2, dict(), dict(), False, True)
    draw_table_2 = bra_from_tr.draw_table(table_2, "竜王戦第01期" + org_tree2.display_name)
    outfile.write(draw_table_2)

    # match_db2 = sql_read.read_match("竜王戦", "第01期", "決勝トーナメント")
    # round_db2 = gen_round_name.read_round("竜王戦", "第01期", "決勝トーナメント")
    # org_tree2 = organized_t.OrganizedTree(match_db2, "決勝トーナメント", round_db2)
    # table_2 = bra_from_tr.generate_bra_pos(org_tree2, dict(), dict(), True, True)
    # draw_table_2 = bra_from_tr.draw_table(table_2, "竜王戦第01期" + org_tree2.display_name)
    # outfile.write(draw_table_2)

    # match_db2 = sql_read.read_match("竜王戦", "第31期", "6組", "昇級者決定戦")
    # round_db2 = gen_round_name.read_round("竜王戦", "第31期", "6組", "昇級者決定戦")
    # org_tree2 = organized_t.OrganizedTree(match_db2, "6組昇級者決定戦", round_db2)
    # table_2 = bra_from_tr.generate_bra_pos(org_tree2, dict(), dict(), True, True)
    # draw_table_2 = bra_from_tr.draw_table(table_2, "竜王戦第31期" + org_tree2.display_name)
    # outfile.write(draw_table_2)

    # match_db2 = sql_read.read_match("竜王戦", "第31期", "6組", "昇級者決定戦")
    # org_tree2 = organized_t.OrganizedTree(match_db2, "6組昇級者決定戦",
    #                                       ["決勝", "06回戦", "05回戦", "04回戦", "03回戦", "02回戦", "01回戦",
    #                                        ])
    # table_2 = bra_from_tr.generate_bra_pos(org_tree2, dict(), dict(), True, True)
    # draw_table_2 = bra_from_tr.draw_table(table_2)
    # outfile.write(draw_table_2)
    outfile.close()
