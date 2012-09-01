#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# DB: Fornece uma interface simples para acesso à bancos de dados.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-02-29
# Modificado em: 2012-01-13 por henriquelima

if __name__ == "__main__":
	import sys
	sys.path.append("/root/")
	from supermegazord.lib import ldapwrap
else:
	from ..lib import ldapwrap

class JupInfo:
	def __init__(self, nid, nome, curso, ingresso):
		self.nid = nid
		self.nome = nome
		self.curso = curso
		self.ingresso = ingresso

	def __str__(self):
		return "NID:" + (" "*8 + str(self.nid))[-8:] + " Curso: " + (str(self.curso) + " "*4)[:4] + (
			" Ingresso: ") + self.ingresso + "; Nome: " + self.nome

	def __repr__(self):
		return "JupInfo(%r)" % self.__dict__
		

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

nidscache = None
def load_nidscache():
	global nidscache
	if nidscache != None: return
	nidscache = ({}, {})
	for line in open(nidsfile):
		# Array 0 = Key: login, value:  NID
		# Array 1 = Key:  NID , value: login
		split = line.strip().split(':')
		if len(split) != 2: continue
		nidscache[0][split[0]] = split[1]
		nidscache[1][split[1]] = split[0]

def login_to_nid(login):
	load_nidscache()
	try:
		return nidscache[0][login]
	except:
		return ''

def nid_to_login(nid):
	load_nidscache()
	try:
		return nidscache[1][nid]
	except:
		return ''

def add_nid_login(nid, login):
	if not nid or not login: return False
	try:
		open(nidsfile, 'a').write(login + ':' + nid + '\n')
		nidscache[0][login] = nid
		nidscache[1][nid] = login
		return True
	except:
		return False

def get_jupinfo_from_nid(nid):
	for source in (jupinfofile, nojupinfofile):
		for line in open(source):
			if nid == line.strip().split(':')[0]:
				return jupinfo_from_raw(line)

def get_jupinfo_from_login(login):
	return get_jupinfo_from_nid(login_to_nid(login))

def get_next_uid():
	MAX_UID = 59999 # reservamos 60000 para cima para propósitos especiais


	# 

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
		print "ERRO: criando mais de 999 contas em um único ano. Caraca, como isso aconteceu!?"
		return ""

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
		open(historyfolder + nid, 'a').write(datetime.date.today().isoformat() + " - " + msg)
		return True
	except:
		return False

def add_history_by_login(login, msg):
	return add_history_by_nid(login_to_nid(login), msg)

def generate_password(length = 10):
	import string
	from random import choice
	chars = string.letters + string.digits
	return choice(string.letters) + ''.join(choice(chars) for _ in xrange(length - 2)) + choice(string.digits)

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
