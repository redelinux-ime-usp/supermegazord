# -*- coding: utf-8 -*-

# Kerberos: Simplifica o acesso ao servidor de Kerberos
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-02

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

from supermegazord.db import path

ROOT_PRINC = "root/admin"
try:
	ROOT_PASS = open(path.MEGAZORD_DB + "secrets/kerberos").read()
except IOError:
	ROOT_PASS = ""

import os

def execute_command(command):
	wrap = "kadmin -p " + ROOT_PRINC + " -w " + ROOT_PASS + " -q '" + command + "'" + ">/dev/null 2>/dev/null"
	return os.system(wrap)

def add_user(user, password):
	return execute_command("addprinc -pw " + password + " " + user)

def change_password(user, password):
	return execute_command("change_password -pw " + password + " " + user)

