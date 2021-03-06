from importdata import former_meijin
from metastruct.__init__ import sql_init
from importjunni import juuni_junni_auto, junni_kisei_auto, junni_shidan_auto
from importjunni import junni_oui_auto, junni_oushou_auto
import gen_config
import importdata.python_mysql_dbconf as db_conf

sql_init()

former_meijin.import_former_meijin()
former_meijin.import_former_ryuou()

gen_conf = gen_config.read_primary_config()
if gen_conf["renew_junni_table"] == "True":
    print('Renew junni table')
    for i in range(7, 78):
        juuni_junni_auto.import_junni(i)

if gen_conf["renew_shidan_junni_table"] == "True":
    print('Renew shidan junni table')
    junni_shidan_auto.import_junni()

if gen_conf["renew_oui_junni_table"] == "True":
    print('Renew oui junni table')
    for i in range(1, 61):
        junni_oui_auto.import_junni(i)

if gen_conf["renew_oushou_junni_table"] == "True":
    print('Renew oushou junni table')
    for i in range(1, 70):
        junni_oushou_auto.import_junni(i)

if gen_conf["renew_kisei_junni_table"] == "True":
    print('Renew kisei junni table')
    for i in range(66, 72):
        junni_kisei_auto.import_junni(i)