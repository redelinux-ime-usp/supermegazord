#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# Tools: Ferramentas utilitárias
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2013-02-18

def log(filename, s):
	import supermegazord.db.path as path
	import datetime
	with open(path.MEGAZORD_DB + "/log/" + filename, "a") as f:
		f.write(str(datetime.datetime.now()) + " - " + s + "\n")

def valida_nid(nid):
	import re
	return re.compile('^[0-9]{4,}$').match(nid) != None

logins_invalidos = ['admin', 'root']

def valida_login(login):
	import re
	return (re.compile('^[a-z]{2,12}$').match(login) != None) and (
		login not in logins_invalidos)

def get_next_uid():
	import datetime
	prefix = str(datetime.datetime.now().year)[-2:]

	def convert_str(prefix, i):
		return prefix + ("000" + str(i))[-3:]
	
	from  ..lib import ldapwrap

	uid = ""
	year_id = 0
	while uid == "":
		year_id += 1

		# Cria um uid que começa com os ultimos 2 digitos do ano e termina com 3 digitos únicos.
		uid = convert_str(prefix, year_id)

		# Verifica se já não existe ninguém com esse ID.
		if ldapwrap.find_user_by_uid(uid):
			uid = ""
	
	if year_id > 999:
		raise Exception("Criando mais de 999 contas em um único ano. Caraca, como isso aconteceu!?")
	
	return uid

def generate_password(length = 10):
	import string
	from random import choice
	chars = string.lowercase + string.digits
	return choice(string.uppercase) + ''.join(choice(chars) for _ in xrange(length - 2)) + choice(string.digits)


def ban_login(login, motivo):
	return False

def unban_login(login):
	return True
