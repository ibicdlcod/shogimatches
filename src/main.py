from bracketgen.meijin import junni
from bracketgen.ryuou import ryuou_write
from importdata import kishi_all, match_mass, birthday
import gen_config


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

    ryuou_conf = gen_config.read_primary_config('config\\config.ini', 'ryuou')
    if ryuou_conf["enabled"] == "True":
        ryuou_write.ryuou_output(int(ryuou_conf["start_iter"]), int(ryuou_conf["end_iter"]))

    for i in range(11, 78):
        if i in range(31, 36):
            continue
        junni.generate_junni_table(i, write=(i != 9))
    # no detail3 until 37期
    # data for 8期 is incomplete

