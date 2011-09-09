#!/bin/sh
DIR="$( cd "$( dirname "$0" )" && pwd )"
MANAG=/homework/manage.py
python $DIR$MANAG syncdb --noinput
python $DIR$MANAG schemamigration profiles --initial
python $DIR$MANAG migrate profiles --fake
#python $DIR$MANAG schemamigration profiles --auto
#python $DIR$MANAG migrate profiles