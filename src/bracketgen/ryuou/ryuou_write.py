from bracketgen.ryuou import ryuou_new, ryuou_old, ryuou_template


def ryuou_output(start_iteration: int, end_iteration: int):
    for i in range(start_iteration, end_iteration + 1):
        outfile_name = f"txt_dst\\ryuou\\usage_{i}.txt"
        outfile = open(outfile_name, 'w', encoding="utf-8-sig")
        j = str(i).zfill(2)
        out_str = ryuou_template.gen_usage(f"第{j}期", [7, 0, 1, 2, 3, 4, 5, 6])
        outfile.write(out_str)
        outfile.close()
    for i in range(min(start_iteration, 19), min(end_iteration + 1, 19)):
        outfile_name = f"txt_dst\\ryuou\\{i}.txt"
        outfile = open(outfile_name, 'w', encoding="utf-8-sig")
        if i == 1:
            out_str = ryuou_template.gen_template(ryuou_old.ryuou_old_str_dict("第01期"))
            outfile.write(out_str)
        else:
            j = str(i).zfill(2)
            j_1 = str(i - 1).zfill(2)
            out_str = ryuou_template.gen_template(ryuou_old.ryuou_old_str_dict(f"第{j}期", f"第{j_1}期"))
            outfile.write(out_str)
        outfile.close()
    for i in range(max(start_iteration, 19), max(end_iteration + 1, 19)):
        outfile_name = f"txt_dst\\ryuou\\{i}.txt"
        outfile = open(outfile_name, 'w', encoding="utf-8-sig")
        j = str(i).zfill(2)
        j_1 = str(i - 1).zfill(2)
        out_str = ryuou_template.gen_template(ryuou_new.ryuou_str_dict(f"第{j}期", f"第{j_1}期"))
        outfile.write(out_str)
        outfile.close()
