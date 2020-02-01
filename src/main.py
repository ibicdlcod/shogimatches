from importdata import former_meijin, kishi_all
from bracketgen.ryuou import ryuou_new, ryuou_old, ryuou_template, ryuou_write
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

    former_meijin.import_former_meijin()
    ryuou_write.ryuou_output(18, 20)