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
	return re.compile('^[a-z]{4,}$').match(login)

jupinfofile   = "/root/supermegazord/db/usuarios/jup_info"
nojupinfofile = "/root/supermegazord/db/usuarios/nojup_info"
nidsfile      = "/root/supermegazord/db/usuarios/nids"
nextuid       = "/root/supermegazord/db/usuarios/nextuid"
suspensoes    = "/root/supermegazord/db/usuarios/suspensoes"
historyfolder = "/root/supermegazord/db/usuarios/historicos/"

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
		open(nidsfile, 'a').write(nid + ':' + login + '\n')
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
	try:
		uid = int(open(nextuid).read().strip())
	except:
		uid = 2000
	from  ..lib import ldapwrap

	# Garante que o UID não está sendo utilizado
	while ldapwrap.find_user_by_uid(uid):
		uid += 1

	if uid == 31415: uid += 1 # Preserva o uid do nub do will

	if uid > MAX_UID:
		print "ERRO: Acabaram as UIDs! Admin, você está numa bela enrascada. Eu não queria ser você."
		# Eu rescrevi esse sistema, mas não me atrevi a mexer nisso, entao deixei a mensagem original. Sinto muito.
		return '-1'
	
	open(nextuid, 'w').write(str(uid + 1))

	return str(uid)

def set_next_uid(uid):
	try:
		open(nextuid, 'w').write(str(uid))
		return True
	except:
		return False

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
	if valida_nid(sys.argv[1]):
		print get_jupinfo_from_nid(sys.argv[1]).nome
	elif valida_login(sys.argv[1]):
		print login_to_nid(sys.argv[1])
	else:
		print "Uso: %s <nid ou login>", sys.argv[0]
