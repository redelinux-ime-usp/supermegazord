#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
from supermegazord.db import users
from supermegazord.lib import ldapwrap
from supermegazord.lib import account

logins = open(sys.argv[1], 'r')
try:
	saida = open(sys.argv[2], 'w')
except:
	saida = open('/dev/stdout', 'w')

MAX_LOGIN = 16
MAX_NAME  = 40

IMORTAIS = ldapwrap.find_grupo_by_name('imortais')
groupnames_cache = dict()
def gid_to_nome(gid):
	global groupnames_cache
	if gid in groupnames_cache: return groupnames_cache[gid]
	try:
		grupo = ldapwrap.find_grupo_by_gid(gid)['cn'][0]
	except:
		grupo = "unk"
	groupnames_cache[gid] = grupo
	return grupo

def get_hist(nid):
		return ''

def colhe_dados(login):
	acc = account.from_login(login)
	result = "Login: %s;" % (login + " " * MAX_LOGIN)[:MAX_LOGIN]
	if acc == None:
		result += " Conta Inexistente"
	else:
		result += " Nome: " + (acc.name + (" " * MAX_NAME))[:MAX_NAME] + ";"
		result += " UID: %s;" % acc.uid
		result += " GID: %s;" % acc.gid
		result += " NID: %s;" % (" " * 7 + users.login_to_nid(login))[-7:]
		result += " Grupo: %s;" % (gid_to_nome(acc.gid) + ' ' * 5)[:5]
		result += get_hist(users.login_to_nid(login))
		if acc.is_in_group_by_ldapdata(IMORTAIS):
			result += " Imortal"
	return result
	
import time

count = 0
start_time = time.time()
for u in logins:
	saida.write(colhe_dados(u.strip()) + "\n")
	count += 1

print "Analisou %d usuários em" % count, "%f segundos." % (time.time() - start_time)
