#!/usr/bin/env python
# -*- coding: utf-8 -*-

# renova_senha: Renova senha de contas da rede a partir de um NID presente no db/users ou de um login.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-02

import sys
sys.path.append("/root/")

from supermegazord.db import users
from supermegazord.lib import cores
from supermegazord.lib import ldapwrap

def wait():
	import getpass
	getpass.getpass("\nPressione ENTER ")

def clear():
	print chr(27) + "[2J"

def wait_and_clear():
	wait()
	clear()

clear()

ldapinfo = None
while ldapinfo == None:
	entrada = raw_input("NID ou Login: ")
	if not entrada: exit()

	login = ""

	if users.valida_nid(entrada):
		login = users.nid_to_login(entrada)

	elif users.valida_login(entrada):
		login = entrada 

	else:
		print "Erro: NID ou Login inválido."
		wait_and_clear()
		continue

	if login: ldapinfo = ldapwrap.find_user_by_login(login)
	if login == "" or not ldapinfo:
		print "Erro: Usuário não encontrado. Alunos que terminaram a graduação não possuem mais contas na rede."
		wait_and_clear()
		continue

clear()

jupinfo = users.get_jupinfo_from_login(ldapinfo['uid'][0])

print "Confirmando dados:"
print
print "NID     : %s" % jupinfo.nid
print "Login   : %s" % ldapinfo['uid'][0]
print "Nome    : %s" % ldapinfo['cn'][0]
print "Grupo   : %s" % jupinfo.curso
print "Ingresso: %s" % jupinfo.ingresso
print
print cores.verm + "AVISO: esse script renovará apenas a senha LDAP do usuário!" + cores.norm
print

confirm = raw_input("Deseja continuar com a renovação de senha? (y/n) ")
if confirm != "y": exit()

newpassword = users.generate_password()

if ldapwrap.change_password(ldapinfo['uid'][0], newpassword) != 0:
	print "Erro mudando senha!"
	exit()

display_login = (ldapinfo['uid'][0] + "          ")[:12]
display_password = newpassword 

print
print " --------------------------------------------------------------------------- "
print "|             Login:   " + cores.verd + display_login + cores.norm + "   | Senha:   " + cores.verd + display_password + cores.norm + "                 |"
print " --------------------------------------------------------------------------- "
print
print cores.verm + "                    Devolva a carteirinha do usuário!" + cores.norm
print
wait()
