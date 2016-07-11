#!/bin/bash

####################
###
### DO NOT PUT THIS FILE ON YOUR OWN PROJECT
###
### Please run this script like Your_Project_Path@host$ bash /yous/scripts/path/deploy.sh
###
####################
cp -f settings.py.sample settings.py

MYSQL_HOST=""
MYSQL_PORT="3306"
MYSQL_USER=""
MYSQL_PASS=""
MYSQL_NAME="cherie"


sed -i s/##MYSQL_default_HOST##/$MYSQL_HOST/g settings.py
sed -i s/##MYSQL_default_PORT##/$MYSQL_PORT/g settings.py
sed -i s/##MYSQL_default_USER##/$MYSQL_USER/g settings.py
sed -i s/##MYSQL_default_PASS##/$MYSQL_PASS/g settings.py
sed -i s/##MYSQL_default_NAME##/$MYSQL_NAME/g settings.py
