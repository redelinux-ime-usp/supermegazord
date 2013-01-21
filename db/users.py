#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# DB: Fornece uma interface simples para acesso à bancos de dados.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-02-29
# Modificado em: 2012-01-13 por henriquelima

import supermegazord.lib.ldapwrap as ldapwrap
from supermegazord.lib.jupinfo import JupInfo

def jupinfo_from_raw(s):
	data = s.strip().split(':')
	try:
		ingresso = data[3]
	except:
		ingresso = "n/a"
	return JupInfo(data[0], data[1], data[2], ingresso)
	

def valida_nid(nid):
	import re
	return re.compile('^[0-9]{4,}$').match(nid)

def valida_login(login):
	import re
	return re.compile('^[a-z]{2,12}$').match(login)

jupinfofile   = "/opt/megazord-db/usuarios/jupiter/jup_info"
nojupinfofile = "/opt/megazord-db/usuarios/jupiter/nojup_info"
nidsfile      = "/opt/megazord-db/usuarios/nids"
suspensoes    = "/opt/megazord-db/usuarios/suspensoes"
historyfolder = "/opt/megazord-db/usuarios/historicos/"

nidscache = ({}, {})
def cache_nid(login, nid):
	# Array 0 = Key: login, value:  NID
	# Array 1 = Key:  NID , value: login
	nidscache[0][login] = nid
	nidscache[1][nid] = login
	

def login_to_nid(login):
	if login in nidscache[0]:
		return nidscache[0][login]
	data = ldapwrap.find_user_by_login(login)
	if data: 
		if 'nid' not in data: return ''
		nid = data['nid'][0]
	else:
		nid = ''
	cache_nid(login, nid)
	return nid

def nid_to_login(nid):
	if nid in nidscache[1]:
		return nidscache[1][nid]
	data = ldapwrap.find_user_by_nid(nid)
	if data: login = data['uid'][0]
	else: login = ''
	cache_nid(login, nid)
	return login

def add_nid_login(nid, login):
	#TODO obsolete
	return False

def get_jupinfo_from_nid(nid):
	for source in (jupinfofile, nojupinfofile):
		for line in open(source):
			if str(nid) == line.strip().split(':')[0]:
				return jupinfo_from_raw(line)

def get_jupinfo_from_login(login):
	return get_jupinfo_from_nid(login_to_nid(login))

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

def ban_login(login, motivo):
	# TODO: fazer
	return False

def unban_login(login):
	newsuspensoes = open(suspensoes + '.tmp', 'w')
	if not newsuspensoes: return False
	try:
		for line in open(suspensoes):
			if login not in line.strip().split(':')[0]:
				newsuspensoes.write(line)
	except:
		return False
	newsuspensoes.close()
	import os
	os.unlink(suspensoes)
	try:
		os.rename(suspensoes + '.tmp', suspensoes)
		return True
	except:
		return False

def add_history_by_nid(nid, msg):
	if not nid: return False
	import datetime
	try:
		open(historyfolder + nid, 'a').write(datetime.datetime.now().isoformat(" ") + " - " + msg + "\n")
		return True
	except:
		return False

def add_history_by_login(login, msg):
	return add_history_by_nid(login_to_nid(login), msg)

def generate_password(length = 10):
	import string
	from random import choice
	chars = string.lowercase + string.digits
	return choice(string.uppercase) + ''.join(choice(chars) for _ in xrange(length - 2)) + choice(string.digits)

if __name__ == "__main__":
	import sys
	if len(sys.argv) != 2:
		print "Uso: %s <nid ou login>" % sys.argv[0]
		exit(1)

	
	try:
		if valida_nid(sys.argv[1]):
			print get_jupinfo_from_nid(sys.argv[1]).nome
		elif valida_login(sys.argv[1]):
			print login_to_nid(sys.argv[1])
	except:
		print "NID ou Login desconhecido"
