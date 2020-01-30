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
    outfile_name = "temp.txt"
    outfile = open(outfile_name, 'w', encoding="utf-8-sig")
    outfile.write(ryuou_old.ryuou_old_str("第02期"))
    outfile.close()
