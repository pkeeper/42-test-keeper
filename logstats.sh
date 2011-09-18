#!/bin/sh

NOW=$(date +"%F")
FILE="./$NOW.dat"

python homework/manage.py modelscount 2> $FILE