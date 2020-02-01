import importdata.kishi_txt as txt


def gen_kishi_db():
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
    return kishi_db
