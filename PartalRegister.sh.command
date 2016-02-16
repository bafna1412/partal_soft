#!/bin/sh
HOST='http://127.0.0.1:8000/partal'
SOURCE='/Users/siddharth/Documents/Python/apps/partal_soft/manage.py'
BROWSER='/Applications/Google Chrome.app'
awhile=2

mysql.server start
sleep $awhile && /usr/bin/open -a "$BROWSER" $HOST & 
python $SOURCE runserver

