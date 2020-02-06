from bracketgen.meijin import junni
from bracketgen.ryuou import ryuou_write
from bracketgen.shidan import shidan_template
from bracketgen.eiou import eiou_template
from bracketgen.oui import oui, oui_template
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

    shidan_conf = gen_config.read_primary_config('config\\config.ini', 'shidan')
    if shidan_conf["enabled"] == "True":
        for i in range(int(shidan_conf["start_iter"]), int(shidan_conf["end_iter"]) + 1):
            result_str = shidan_template.shidan_str(i)
            outfile1_name = f"txt_dst\\shidan\\{i}.txt"
            outfile2_name = f"txt_dst\\shidan\\usage_{i}.txt"
            outfile1 = open(outfile1_name, "w", encoding="utf-8-sig")
            outfile2 = open(outfile2_name, "w", encoding="utf-8-sig")
            outfile1.write(result_str[0])
            outfile2.write(result_str[1])
            outfile1.close()
            outfile2.close()

    kudan_conf = gen_config.read_primary_config('config\\config.ini', 'kudan')
    if kudan_conf["enabled"] == "True":
        for i in range(int(kudan_conf["start_iter"]), int(kudan_conf["end_iter"]) + 1):
            result_str = shidan_template.kudan_str(i)
            outfile1_name = f"txt_dst\\kudan\\{i}.txt"
            outfile2_name = f"txt_dst\\kudan\\usage_{i}.txt"
            outfile1 = open(outfile1_name, "w", encoding="utf-8-sig")
            outfile2 = open(outfile2_name, "w", encoding="utf-8-sig")
            outfile1.write(result_str[0])
            outfile2.write(result_str[1])
            outfile1.close()
            outfile2.close()
    
    eiou_conf = gen_config.read_primary_config('config\\config.ini', 'eiou')
    if eiou_conf["enabled"] == "True":
        for i in range(int(eiou_conf["start_iter"]), int(eiou_conf["end_iter"]) + 1):
            result_str = eiou_template.eiou_str(i)
            outfile1_name = f"txt_dst\\eiou\\{i}.txt"
            outfile2_name = f"txt_dst\\eiou\\usage_{i}.txt"
            outfile1 = open(outfile1_name, "w", encoding="utf-8-sig")
            outfile2 = open(outfile2_name, "w", encoding="utf-8-sig")
            outfile1.write(result_str[0])
            outfile2.write(result_str[1])
            outfile1.close()
            outfile2.close()
            
    oui_conf = gen_config.read_primary_config('config\\config.ini', 'oui')
    if oui_conf["enabled"] == "True":
        for i in range(int(oui_conf["start_iter"]), int(oui_conf["end_iter"]) + 1):
            result_str = oui_template.oui_str(i)
            outfile1_name = f"txt_dst\\oui\\{i}.txt"
            outfile2_name = f"txt_dst\\oui\\usage_{i}.txt"
            outfile1 = open(outfile1_name, "w", encoding="utf-8-sig")
            outfile2 = open(outfile2_name, "w", encoding="utf-8-sig")
            outfile1.write(result_str[0])
            outfile2.write(result_str[1])
            outfile1.close()
            outfile2.close()
            
    # for i in range(19, 61):
    #     outfile_name = f"txt_dst\\oui\\{i}.txt"
    #     outfile = open(outfile_name, "w", encoding="utf-8-sig")
    #     for k, v in oui.oui_str_dict(i).items():
    #         outfile.write(k + "\n")
    #         outfile.write(v)
    #     outfile.close()
