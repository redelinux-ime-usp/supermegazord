#!/bin/bash
SUPERMEGAZORD=/root/supermegazord/
MACHINES=`$SUPERMEGAZORD/db/machines.py all`

DB="/root/redelinux/estatisticas/login/`date -d '1 month ago' +'%Y-%m'`"

mkdir -p $DB

for m in $MACHINES; do
	echo -n $m
	scp $m:/var/log/wtmp.1 $DB/$m
done
