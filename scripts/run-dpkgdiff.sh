#!/bin/bash
#MACHINES=$(/opt/supermegazord/db/machines.py clients)
MACHINES=$(/opt/bin/watchman --up clients)
MAIN=$(head -n1 <<< "$MACHINES")
mkdir -p dpkg
rm -f diffdpkg
touch diffdpkg
for m in $MACHINES
do 
	echo $m
	/opt/bin/rlstats $m pacotes > dpkg/$m

	echo $m >> diffdpkg
	diff dpkg/$MAIN dpkg/$m >> diffdpkg
	echo >> diffdpkg
done
