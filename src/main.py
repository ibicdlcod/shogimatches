from datetime import date

from bracketgen.meijin import junni
from bracketgen.ryuou import ryuou_write
from bracketgen.shidan import shidan_template
from importdata import birthday, kishi_all, match_mass, sql_read, match_auto
import gen_config
from metastruct.match_data import Match

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

    junni_conf = gen_config.read_primary_config('config\\config.ini', 'junni')
    if junni_conf["enabled"] == "True":
        for i in range(int(junni_conf["start_iter"]), int(junni_conf["end_iter"]) + 1):
            if i in range(31, 36):
                continue
            junni.generate_junni_table(i, write=(i != int(junni_conf["start_iter"])))

    for i in range(1, 27):
        result_str = shidan_template.shidan_str(i)
        outfile1_name = f"txt_dst\\shidan\\{i}.txt"
        outfile2_name = f"txt_dst\\shidan\\usage_{i}.txt"
        outfile1 = open(outfile1_name, "w", encoding="utf-8-sig")
        outfile2 = open(outfile2_name, "w", encoding="utf-8-sig")
        outfile1.write(result_str[0])
        outfile2.write(result_str[1])
        outfile1.close()
        outfile2.close()
