from importdata import former_meijin
from metastruct.__init__ import sql_init
import importdata.python_mysql_dbconf as db_conf

sql_init()

former_meijin.import_former_meijin()
former_meijin.import_former_ryuou()
