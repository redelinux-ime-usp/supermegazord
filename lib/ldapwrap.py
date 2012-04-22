# -*- coding: utf-8 -*-

# LDAP: Simplifica o acesso ao servidor de LDAP
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-02-29

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

from supermegazord.db import path

BASEDN = "dc=linux,dc=ime,dc=usp,dc=br"
URI	   = "ldap://ldap"
ROOTDN = "cn=admin,dc=linux,dc=ime,dc=usp,dc=br"
try:
	ROOTPW = open(path.MEGAZORD_DB + "secrets/ldap").read()
except IOError:
	ROOTPW = None

import ldap
from ldap import modlist

def open_connection():
	con = ldap.initialize(URI)
	if ROOTPW != None:
		con.simple_bind_s(ROOTDN, ROOTPW)
	return con

def query(target, restriction = ''):
	con = open_connection()
	try:
		return con.search_s(target + ',' + BASEDN, ldap.SCOPE_SUBTREE, restriction)
	except:
		return None

def find_user_by_restriction(restriction):
	con = open_connection()
	try:
		return query('ou=People', restriction)[0][1]
	except:
		return None

def find_user_by_uid(uid):
	return find_user_by_restriction('uidNumber=%s' % uid)

def find_user_by_login(login):
	return find_user_by_restriction('uid=%s' % login)

def add_user(account):
	attrs = {}
	attrs['objectClass'] = ['account', 'posixAccount', 'top', 'shadowAccount']
	try:
		attrs['cn'] = account.name
		attrs['uid'] = account.login
		attrs['uidNumber'] = str(account.uid)
		attrs['gidNumber'] = str(account.gid)
		attrs['homeDirectory'] = account.home
		attrs['loginShell'] = account.shell
		if account.password != '':
			attrs['userPassword'] = account.password
	except:
		return False

	try:
		ldif = modlist.addModlist(attrs)
	except:
		return False

	try:
		dn = "uid=" + attrs['uid'] + ",ou=People,dc=linux,dc=ime,dc=usp,dc=br"
		open_connection().add_s(dn, ldif)
		return True
	except:
		return False
	return False

def find_grupo_by_gid(gid):
	try:
		return query('ou=Group', 'gidNumber=%s' % gid)[0][1]
	except:
		return None

def find_grupo_by_name(name):
	try:
		return query('ou=Group', 'cn=%s' % name)[0][1]
	except:
		return None

def get_gid(curso):
	try:
		return find_grupo_by_name(curso)['gidNumber'][0]
	except:
		return -1

def change_password(user, password):
	import os
	command = "ldappasswd -D "+ROOTDN+" -w"+ROOTPW+" uid=" + user + ",ou=People," + BASEDN + " -s" + password
	return os.system(command)

