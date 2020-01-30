import importdata.kishi_txt as txt
from importdata import python_mysql_dbconf
from bracketgen import ryuou_old
import database_fix

if __name__ == '__main__':
    gen_conf = python_mysql_dbconf.read_db_general_config()
    update_on = gen_conf["read_update_on"]

    database_fix.fix_database()

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

        outfile_name = "txt_src\\names2.csv"
        outfile = open(outfile_name, 'w', encoding="utf-8-sig")
        for i in kishi_db:
            outfile.write(str(i) + "\n")
        outfile.close()
    for i in range(1, 2):
        outfile_name = f"txt_dst\\ryuou\\{i}.txt"
        outfile = open(outfile_name, 'w', encoding="utf-8-sig")
        if i == 1:
            outfile.write(ryuou_old.ryuou_old_str("第01期"))
        else:
            j = str(i).zfill(2)
            j_1 = str(i-1).zfill(2)
            outfile.write(ryuou_old.ryuou_old_str(f"第{j}期", f"第{j_1}期"))
        outfile.close()
