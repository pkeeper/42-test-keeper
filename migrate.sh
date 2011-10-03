#!/bin/sh
sh ../uwsgi/post_deploy.sh
python ./homework/manage.py sqlclear auth south sites admin profiles | python ./homework/manage.py dbshell
python ./homework/manage.py syncdb --noinput
python ./homework/manage.py loaddata homework/Tinitial_data.json homework/profiles/fixtures/Tinitial_data.json
python ./homework/manage.py migrate modelslog 0001_initial --fake
python ./homework/manage.py migrate
exit 0