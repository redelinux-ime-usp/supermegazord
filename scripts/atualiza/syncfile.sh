#!/bin/bash

MACHINES_SCRIPT="/root/supermegazord/db/machines.py"

TARGET_GROUP='clients'
while getopts ":t:" opt; do
	case $opt in
		t)
			TARGET_GROUP="$OPTARG"
			;;
		\?)
			echo "Opção inválida: -$OPTARG"
			exit 1
			;;
		:)
			echo "Opção -$OPTARG precisa de um argumento."
			exit 1
			;;
	esac
done

#/root/supermegazord/db/machines.py $TARGET
SOURCE_PATH=""
TARGET_PATH=""

while [ "$#" -gt 0 ]; do
	case $1 in
		-*) if [ "$1" == "-t" ]; then
				shift;
			fi
			;;
		*)  if [ "$SOURCE_PATH" == "" ]; then
				SOURCE_PATH=$1
			elif [ "$TARGET_PATH" == "" ]; then
				TARGET_PATH=$1
			else
				echo "Erro: argumentos demais."
				exit 1
			fi
			;;
	esac
	shift;
done
if [ "$TARGET_PATH" == "" ]; then
	echo "Uso: syncfile.sh [-t GRUPO] source target_path"
	exit 1
fi

#echo "Copiando $SOURCE_PATH para $TARGET_PATH de $TARGET_GROUP"
for m in $($MACHINES_SCRIPT $TARGET_GROUP); do
	echo -n "$m: "
	scp $SOURCE_PATH $m:$TARGET_PATH
done
