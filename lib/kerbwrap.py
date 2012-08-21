# -*- coding: utf-8 -*-

# Kerberos: Simplifica o acesso ao servidor de Kerberos
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-02

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

from supermegazord.db import path

ROOT_PRINC = "root/admin"
ROOT_FILE  = path.MEGAZORD_DB + "secrets/kerberos"
LOG_FILE = "/var/log/supermegazord.log"

import os

def execute_command(command):
	wrap = "kadmin -p " + ROOT_PRINC + " -q '" + command + "'" + ">>" + LOG_FILE + " 2>>" + LOG_FILE + "<" + ROOT_FILE
	return os.system(wrap)

def user_exists(user):
	import subprocess
	p = subprocess.Popen(["kadmin", "-p" + ROOT_PRINC, "-q getprinc " + user], stdin=open(ROOT_FILE), stderr=subprocess.PIPE, stdout=open('/dev/null'))
	out, err = p.communicate()
	return err.find("Principal does not exist while retrieving") == -1

def add_user(user, password):
	return execute_command("addprinc -pw " + password + " " + user)

def change_password(user, password):
	return execute_command("change_password -pw " + password + " " + user)

