from metastruct import kishi_data
import importdata.python_mysql_dbconf as db_conf
import mysql.connector


def process_txt():
    kishi_db = []
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
        kishi_db.append(kishi_data.Kishi(id_1, fullname, 2, "", False, False, False))
        content = infile.readline()
    kishi_db.sort(key=lambda x: x.id)
    infile.close()
    return kishi_db


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
            index2 = line1.find("\"", index1 + 1)
            returns.append(int(line1[index1 + 6:index2]))

        line1 = infile1.readline()
    infile1.close()
    returns.sort()
    return returns


def sql_connect(insert_first: bool = False,
                read: bool = False,
                kishi_db=None):
    """ Connect to MySQL database """

    if kishi_db is None:
        kishi_db = []
    db_config = db_conf.read_db_config()
    conn = None

    query_establish = ("CREATE DATABASE IF NOT EXISTS shogi\n"
                       "CHARACTER SET utf8mb4;\n"
                       + "USE shogi;\n"
                       + "CREATE TABLE IF NOT EXISTS kishi(\n"
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
            gen_conf = db_conf.read_general_config()
            if gen_conf["sql_output"] == "True":
                print('Connected to MySQL database')

        cursor = conn.cursor()
        cursor.execute(query_establish, args_establish, multi=True)

        if insert_first:
            query_insert = "INSERT INTO kishi(id,fullname,surname_len,wiki_name," \
                           "woman,current_shoreikai,current_amateur)\n" \
                           "VALUES(%s,%s,%s,%s,%s,%s,%s)\n" \
                           "ON DUPLICATE KEY UPDATE " \
                           "fullname=VALUES(fullname)," \
                           "woman=VALUES(woman)," \
                           "current_shoreikai=VALUES(current_shoreikai)," \
                           "current_amateur=VALUES(current_amateur);"
            for kishi1 in kishi_db:
                args_insert = (kishi1.id, kishi1.fullname, kishi1.surname_length,
                               kishi1.wiki_name, kishi1.woman, kishi1.current_shoreikai,
                               kishi1.current_amateur)
                cursor = conn.cursor()
                cursor.execute(query_insert, args_insert)

            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')  # Expected behaviour

        if read:
            cursor.execute("SELECT * FROM kishi")

            row = cursor.fetchone()
            while row is not None:
                current_id = row[0]
                current_kishi: kishi_data.Kishi = [kishi1 for kishi1 in kishi_db if kishi1.id == current_id][0]
                current_kishi.fullname = row[1]
                current_kishi.surname_length = row[2]
                current_kishi.wiki_name = row[3]
                current_kishi.woman = (row[4] == 1)
                current_kishi.current_shoreikai = (row[5] == 1)
                current_kishi.current_amateur = (row[6] == 1)
                row = cursor.fetchone()
        cursor.close()

        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return kishi_db
