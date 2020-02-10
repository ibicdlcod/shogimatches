from bracketgen.eiou import eiou_template
from bracketgen.kiou import kiou_template
from bracketgen.kisei import kisei_template
from bracketgen.meijin import junni
from bracketgen.oui import oui_template
from bracketgen.oushou import oushou_template
from bracketgen.ouza import ouza_template
from bracketgen.ryuou import ryuou_write
from bracketgen.shidan import shidan_template
import gen_config


def content():
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

    ouza_conf = gen_config.read_primary_config('config\\config.ini', 'ouza')
    if ouza_conf["enabled"] == "True":
        for i in range(int(ouza_conf["start_iter"]), int(ouza_conf["end_iter"]) + 1):
            result_str = ouza_template.ouza_str(i)
            outfile1_name = f"txt_dst\\ouza\\{i}.txt"
            outfile2_name = f"txt_dst\\ouza\\usage_{i}.txt"
            outfile1 = open(outfile1_name, "w", encoding="utf-8-sig")
            outfile2 = open(outfile2_name, "w", encoding="utf-8-sig")
            outfile1.write(result_str[0])
            outfile2.write(result_str[1])
            outfile1.close()
            outfile2.close()

    kiou_conf = gen_config.read_primary_config('config\\config.ini', 'kiou')
    if kiou_conf["enabled"] == "True":
        for i in range(int(kiou_conf["start_iter"]), int(kiou_conf["end_iter"]) + 1):
            result_str = kiou_template.kiou_str(i)
            outfile1_name = f"txt_dst\\kiou\\{i}.txt"
            outfile2_name = f"txt_dst\\kiou\\usage_{i}.txt"
            outfile1 = open(outfile1_name, "w", encoding="utf-8-sig")
            outfile2 = open(outfile2_name, "w", encoding="utf-8-sig")
            outfile1.write(result_str[0])
            outfile2.write(result_str[1])
            outfile1.close()
            outfile2.close()

    oushou_conf = gen_config.read_primary_config('config\\config.ini', 'oushou')
    if oushou_conf["enabled"] == "True":
        for i in range(int(oushou_conf["start_iter"]), int(oushou_conf["end_iter"]) + 1):
            result_str = oushou_template.oushou_str(i)
            outfile1_name = f"txt_dst\\oushou\\{i}.txt"
            outfile2_name = f"txt_dst\\oushou\\usage_{i}.txt"
            outfile1 = open(outfile1_name, "w", encoding="utf-8-sig")
            outfile2 = open(outfile2_name, "w", encoding="utf-8-sig")
            outfile1.write(result_str[0])
            outfile2.write(result_str[1])
            outfile1.close()
            outfile2.close()

    kisei_conf = gen_config.read_primary_config('config\\config.ini', 'kisei')
    if kisei_conf["enabled"] == "True":
        for i in range(int(kisei_conf["start_iter"]), int(kisei_conf["end_iter"]) + 1):
            result_str = kisei_template.kisei_str(i)
            outfile1_name = f"txt_dst\\kisei\\{i}.txt"
            outfile2_name = f"txt_dst\\kisei\\usage_{i}.txt"
            outfile1 = open(outfile1_name, "w", encoding="utf-8-sig")
            outfile2 = open(outfile2_name, "w", encoding="utf-8-sig")
            outfile1.write(result_str[0])
            outfile2.write(result_str[1])
            outfile1.close()
            outfile2.close()
