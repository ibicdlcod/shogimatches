from bracketgen import lea_from_mat, gen_round_name
from bracketgen.ryuou import ryuou_write
from importdata import kishi_all, sql_read
import gen_config

if __name__ == '__main__':
    gen_conf = gen_config.read_primary_config()
    update_on = (gen_conf["read_update_on"] == "True")

    if update_on:
        kishi_db = kishi_all.gen_kishi_db()

        outfile_name = "txt_src\\names2.csv"
        outfile = open(outfile_name, 'w', encoding="utf-8-sig")
        for i in kishi_db:
            outfile.write(str(i) + "\n")
        outfile.close()

    ryuou_conf = gen_config.read_primary_config('config\\config.ini', 'ryuou')
    if ryuou_conf["enabled"] == "True":
        ryuou_write.ryuou_output(int(ryuou_conf["start_iter"]), int(ryuou_conf["end_iter"]))

    junni_matches = sql_read.read_match("順位戦", "第77期", "C級2組")
    junni_round = gen_round_name.read_round("順位戦", "第77期", "C級2組", league=True)
    lea_from_mat.generate_lea_pos(junni_matches, None, junni_round, "C級2組")