from importdata import former_meijin, juuni_junni_auto
from metastruct.__init__ import sql_init
import gen_config
import importdata.python_mysql_dbconf as db_conf

sql_init()

former_meijin.import_former_meijin()
former_meijin.import_former_ryuou()

gen_conf = gen_config.read_primary_config()
if gen_conf["renew_junni_table"] == "True":
    print('Renew former junni table')
    for i in range(7, 78):
        juuni_junni_auto.import_junni(i)