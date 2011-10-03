#!/bin/sh
sh ../uwsgi/post_deploy.sh
python ./homework/manage.py sqlclear auth sites modelslog requests admin contenttypes profiles | python ./homework/manage.py dbshell
python ./homework/manage.py syncdb --noinput
python ./homework/manage.py loaddata homework/Tinitial_data.json homework/profiles/fixtures/Tinitial_data.json
exit 0