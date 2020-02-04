import importdata.python_mysql_dbconf as db_conf
import mysql.connector


def sql_init():
    """ Connect to MySQL database """

    # running as main
    db_config = db_conf.read_db_config()
    # running as import data
    # db_config = db_conf.read_db_config()
    conn = None

    query_init_db = ("CREATE DATABASE IF NOT EXISTS shogi\n"
                     "CHARACTER SET utf8mb4;"
                     "USE shogi;")
    args_init_db = tuple()
    query_init_kishi_table = ("CREATE TABLE IF NOT EXISTS kishi("
                              "id INT,"
                              "fullname VARCHAR(63) NOT NULL,"
                              "surname_len INT DEFAULT 2,"
                              "wiki_name VARCHAR(63),"
                              "woman TINYINT(1) NOT NULL DEFAULT 0,"
                              "current_shoreikai TINYINT(1) NOT NULL DEFAULT 0,"
                              "current_amateur TINYINT(1) NOT NULL DEFAULT 0,"
                              "birthday DATE,"
                              "PRIMARY KEY (id)"
                              ");")
    args_init_kishi_table = tuple()
    query_init_match_table = ("CREATE TABLE IF NOT EXISTS matches("
                              "hash BINARY(64),"
                              "fiscal_year INT NOT NULL DEFAULT 1900,"
                              "match_date DATE NOT NULL DEFAULT '1900-01-01',"
                              "win_loss_for_black TINYINT NOT NULL DEFAULT 1,"
                              "forfeit_active TINYINT(1) NOT NULL DEFAULT 0,"
                              "black_name VARCHAR(63),"
                              "white_name VARCHAR(63),"
                              "iteration VARCHAR(63),"
                              "tournament_name VARCHAR(63),"
                              "detail1 VARCHAR(63),"
                              "detail2 VARCHAR(63),"
                              "detail3 VARCHAR(63),"
                              "mochishogi INT NOT NULL DEFAULT 0,"
                              "sennichite INT NOT NULL DEFAULT 0,"
                              "PRIMARY KEY (hash)"
                              ");")
    args_init_match_table = tuple()
    query_init_rank_table = ("CREATE TABLE IF NOT EXISTS ranking("
                             "id_hash BINARY(64),"
                             "id INT,"
                             "on_date DATE NOT NULL DEFAULT '1900-01-01',"
                             "rank_text VARCHAR(63),"
                             "PRIMARY KEY (id_hash)"
                             ");")
    args_init_rank_table = tuple()
    query_init_former_table = ("CREATE TABLE IF NOT EXISTS former("
                               "tournament_name VARCHAR(63),"
                               "iteration_int INT,"
                               "end_date DATE NOT NULL DEFAULT '1900-01-01',"
                               "winner_fullname VARCHAR(63),"
                               "PRIMARY KEY (end_date)"
                               ");")
    args_init_former_table = tuple()
    query_init_junni_table = ("CREATE TABLE IF NOT EXISTS junni("
                              "id_hash BINARY(64),"
                              "iteration_int INT,"
                              "tier VARCHAR(63),"
                              "junni INT,"
                              "kishi_id INT,"
                              "relegation_point_added TINYINT(1) NOT NULL DEFAULT 0,"
                              "current_relegation_point INT,"
                              "result VARCHAR(63),"
                              "to_fc_year INT,"
                              "PRIMARY KEY (id_hash)"
                              ");")
    args_init_junni_table = tuple()
    query_init_junni_other_table = ("CREATE TABLE IF NOT EXISTS junni_other("
                                    "id_hash BINARY(64),"
                                    "tournament_name VARCHAR(63),"
                                    "iteration VARCHAR(63),"
                                    "junni INT,"
                                    "kishi_id INT,"
                                    "result VARCHAR(63),"
                                    "PRIMARY KEY (id_hash)"
                                    ");")
    args_init_junni_other_table = tuple()

    try:
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            print('Initializing MySQL database')

        cursor = conn.cursor()
        cursor.execute(query_init_db, args_init_db, multi=True)
        print("Database init success")
        cursor.execute(query_init_kishi_table, args_init_kishi_table)
        print("Kishi table init success")
        cursor.execute(query_init_match_table, args_init_match_table)
        print("Match table init success")
        cursor.execute(query_init_rank_table, args_init_rank_table)
        print("Rank table init success")
        cursor.execute(query_init_former_table, args_init_former_table)
        print("Former table init success")
        cursor.execute(query_init_junni_table, args_init_junni_table)
        print("Junni table init success")
        cursor.execute(query_init_junni_other_table, args_init_junni_other_table)
        print("Junni table (non meijin) init success")

        cursor.close()

        conn.commit()

    except mysql.connector.Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
