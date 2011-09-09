#!/bin/sh
#python ./homework/manage.py schemamigration profiles --initial
#python ./homework/manage.py migrate profiles --fake
python ./homework/manage.py schemamigration profiles --auto
python ./homework/manage.py migrate profiles