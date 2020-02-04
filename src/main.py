from bracketgen.meijin import junni
from bracketgen.ryuou import ryuou_write
from bracketgen.shidan import shidan_5_15, shidan_16_26
from importdata import birthday, kishi_all, match_mass
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

    junni_conf = gen_config.read_primary_config('config\\config.ini', 'junni')
    if junni_conf["enabled"] == "True":
        for i in range(int(junni_conf["start_iter"]), int(junni_conf["end_iter"]) + 1):
            if i in range(31, 36):
                continue
            junni.generate_junni_table(i, write=(i != int(junni_conf["start_iter"])))

    for i in range(5, 27):
        outfile_name = f"txt_dst\\shidan\\{i}.txt"
        outfile = open(outfile_name, "w", encoding="utf-8-sig")
        if i >= 16:
            result = shidan_16_26.shidan_str_dict(i)
        else:
            result = shidan_5_15.shidan_str_dict(i)
        out_str = result[7]
        outfile.write(out_str)
        if i >= 16:
            out_str = result[1]
            outfile.write(out_str)
        else:
            out_str = result[3]
            outfile.write(out_str)
            out_str = result[2]
            outfile.write(out_str)
            out_str = result[1]
            outfile.write(out_str)
        outfile.close()
    # no detail3 until 37期
    # data for 8期 is incomplete

