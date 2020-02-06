from importjunni import juuni_junni_auto, junni_shidan_auto, junni_oui_auto
import gen_config

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