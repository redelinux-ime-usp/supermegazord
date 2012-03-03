# -*- coding: utf-8 -*-

# LDAP: Simplifica o acesso ao servidor de LDAP
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-02-29

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

BASEDN = "dc=linux,dc=ime,dc=usp,dc=br"
URI	   = "ldap://ldap"
ROOTDN = "cn=admin,dc=linux,dc=ime,dc=usp,dc=br"
ROOTPW = open("/etc/supermegazord-ldap.secret").read()

import ldap
from ldap import modlist

def open_connection():
	con = ldap.initialize(URI)
	con.simple_bind_s(ROOTDN, ROOTPW)
	return con

def find_user_by_restriction(restriction):
	con = open_connection()
	try:
		return con.search_s('ou=People,' + BASEDN, ldap.SCOPE_SUBTREE, restriction)[0][1]
	except:
		return None

def find_user_by_uid(uid):
	return find_user_by_restriction('uidNumber=%s' % uid)

def find_user_by_login(login):
	return find_user_by_restriction('uid=%s' % login)

def add_user(userdata):
	attrs = {}
	attrs['objectClass'] = ['account', 'posixAccount', 'top', 'shadowAccount']
	try:
		attrs['cn'] = userdata['nome']
		attrs['uid'] = userdata['login']
		attrs['loginShell'] = userdata['shell']
		attrs['uidNumber'] = str(userdata['uid'])
		attrs['gidNumber'] = userdata['gid']
		attrs['homeDirectory'] = userdata['home']
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

def get_gid(curso):
	con = open_connection()
	try:
		return con.search_s('ou=Group,' + BASEDN, ldap.SCOPE_SUBTREE, 'cn=%s' % curso)[0][1]['gidNumber'][0]
	except:
		return -1
