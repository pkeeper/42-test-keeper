#!/bin/sh
sh ../uwsgi/post_deploy.sh
python ./homework/manage.py sqlclear auth sites modelslog requests admin contenttypes profiles south | python ./homework/manage.py dbshell
python ./homework/manage.py syncdb --noinput
python ./homework/manage.py migrate
exit 0