import importdata
from metastruct import kisei_data
import metastruct.python_mysql_dbconf as db_conf
import mysql.connector
from datetime import date

kisei_db = []


def process_txt():
    infile_name = "..\\txt_src\\names.txt"
    infile = open(infile_name, 'r', encoding="utf-8-sig")
    content = infile.readline()
    while content:
        index1 = content.find("\"")
        index2 = content.find("\"", index1 + 1)
        index3 = content.find(">")
        index4 = content.find("(")
        if index4 == -1:
            index4 = content.find("<", index3 + 1)
        id_1 = int(content[index1 + 1:index2])
        fullname = content[index3 + 1:index4]
        kisei_db.append(kisei_data.Kisei(id_1, fullname, 2, "", False, False, False))
        content = infile.readline()
    kisei_db.sort(key=lambda x: x.id)
    infile.close()


def process_more_txt(source_name: str) -> list:
    returns = []
    infile_name1 = f"..\\txt_src\\{source_name}.txt"
    infile1 = open(infile_name1, 'r', encoding="utf-8-sig")
    line1 = infile1.readline()
    while line1:
        index1 = line1.find("?name=")
        if index1 == -1:
            line1 = infile1.readline()
            continue
        else:
            index2 = line1.find("\"", index1+1)
            returns.append(int(line1[index1+6:index2]))

        line1 = infile1.readline()
    infile1.close()
    returns.sort()
    return returns


def sql_connect(insert_first, read):
    """ Connect to MySQL database """

    db_config = db_conf.read_db_config()
    conn = None

    query_establish = ("CREATE DATABASE IF NOT EXISTS shogi\n"
                       "CHARACTER SET utf8mb4;\n"
                       + "USE shogi;\n"
                       + "CREATE TABLE IF NOT EXISTS kisei(\n"
                       + "id INT,\n"
                       + "fullname VARCHAR(255) NOT NULL,\n"
                       + "surname_len INT DEFAULT 2,\n"
                       + "wiki_name VARCHAR(255),\n"
                       + "woman TINYINT(1) NOT NULL DEFAULT 0,"
                       + "current_shoreikai TINYINT(1) NOT NULL DEFAULT 0,"
                       + "current_amateur TINYINT(1) NOT NULL DEFAULT 0,"
                       + "PRIMARY KEY (id)\n"
                       + ");")
    args_establish = tuple()

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connected to MySQL database')

        cursor = conn.cursor()
        cursor.execute(query_establish, args_establish, multi=True)

        if insert_first:
            query_insert = "INSERT INTO kisei(id,fullname,surname_len,wiki_name," \
                           "woman,current_shoreikai,current_amateur)\n" \
                           "VALUES(%s,%s,%s,%s,%s,%s,%s)\n" \
                           "ON DUPLICATE KEY UPDATE " \
                           "fullname=VALUES(fullname)," \
                           "woman=VALUES(woman)," \
                           "current_shoreikai=VALUES(current_shoreikai)," \
                           "current_amateur=VALUES(current_amateur);"
            for kisei1 in kisei_db:
                args_insert = (kisei1.id, kisei1.fullname, kisei1.surname_length,
                               kisei1.wiki_name, kisei1.woman, kisei1.current_shoreikai,
                               kisei1.current_amateur)
                cursor = conn.cursor()
                cursor.execute(query_insert, args_insert)

            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')  # Expected behaviour

        if read:
            cursor.execute("SELECT * FROM kisei")

            row = cursor.fetchone()
            while row is not None:
                current_id = row[0]
                current_kisei: kisei_data.Kisei = [kisei1 for kisei1 in kisei_db if kisei1.id == current_id][0]
                current_kisei.fullname = row[1]
                current_kisei.surname_length = row[2]
                current_kisei.wiki_name = row[3]
                current_kisei.woman = (row[4] == 1)
                current_kisei.current_shoreikai = (row[5] == 1)
                current_kisei.current_amateur = (row[6] == 1)
                row = cursor.fetchone()
        cursor.close()

        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == '__main__':
    update_on = False
    if update_on:
        process_txt()
        amateur1 = process_more_txt("current_amateur_part")
        amateur_w = process_more_txt("current_amateur_woman")
        former_srk = process_more_txt("former_shoreikai")
        current_3dan = process_more_txt("sandan")
        women = process_more_txt("woman")

        for kisei in kisei_db:
            i = kisei.id
            if i in amateur1 or i in amateur_w or i in former_srk:
                kisei.current_amateur = True
            if i in amateur_w or i in women or kisei.fullname == "西山朋佳":
                """
                Special treatment, eh?
                note shoreikai members < 3dan does not appear.
                中七海 and 今井絢 is still treated as amateurs by http://kenyu1234.php.xdomain.jp/
                """
                kisei.woman = True
            if i in current_3dan:
                kisei.current_shoreikai = True

        sql_connect(False, True)

        outfile_name = "..\\txt_src\\names2.csv"
        outfile = open(outfile_name, 'w', encoding="utf-8-sig")
        for i in kisei_db:
            outfile.write(str(i) + "\n")
        outfile.close()

    # outfile1_name = "..\\temp.txt"
    # outfile1 = open(outfile1_name, 'w', encoding="utf-8-sig")
    # str1 = import_ryuou.import_data(1)
    # outfile1.write(str1)
    # outfile1.close()

    # outfile2_name = "..\\temp.txt"
    # outfile2 = open(outfile2_name, 'w', encoding="utf-8-sig")
    # fengdao = [kisei for kisei in kisei_db if kisei.fullname == "豊島将之"][0]
    # str2 = fengdao.rank(date.fromisoformat("2019-12-12"))
    # outfile2.write(str2)
    # outfile2.close()