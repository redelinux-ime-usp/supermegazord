# -*- coding: utf-8 -*-

# LDAP: Simplifica o acesso ao servidor de LDAP
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-02-29

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

from supermegazord.db import path
import json

with open(path.MEGAZORD_DB + "/conf/ldap.conf", "r") as f:
	fulldata = json.load(f)
	

DEFAULT_SHELL = "/bin/bash"
BASEDN	= fulldata['BASEDN']
URI	  	= fulldata['URI']
ROOTDN	= fulldata['ROOTDN']
try:
	ROOTPW = open(path.MEGAZORD_DB + "secrets/ldap").read()
except IOError:
	ROOTPW = None

import ldap
from ldap import modlist

def is_admin():
	return ROOTPW != None

def open_connection():
	con = ldap.initialize(URI)
	if ROOTPW != None:
		con.simple_bind_s(ROOTDN, ROOTPW)
	return con

def query(target, restriction = None, con = None):
	if con == None:
		con = open_connection()
	if restriction:
		return con.search_s(target + ',' + BASEDN, ldap.SCOPE_SUBTREE, restriction)
	else:
		return con.search_s(target + ',' + BASEDN, ldap.SCOPE_SUBTREE)

def find_user_by_restriction(restriction):
	con = open_connection()
	try:
		return query('ou=People', restriction)[0][1]
	except IndexError:
		return None

def find_user_by_uid(uid):
	return find_user_by_restriction('uidNumber=%s' % uid)

def find_user_by_login(login):
	return find_user_by_restriction('uid=%s' % login)

def find_user_by_nid(nid):
	return find_user_by_restriction('nid=%s' % nid)

def add_user(account):
	if account.nid == None: return False
	attrs = {}
	attrs['objectClass'] = ['account', 'posixAccount', 'top', 'shadowAccount', 'megazordAccount']
	attrs['cn'] = str(account.name)
	attrs['uid'] = str(account.login)
	attrs['uidNumber'] = str(account.uid)
	attrs['gidNumber'] = str(account.group.gid)
	attrs['homeDirectory'] = str(account.home)
	attrs['loginShell'] = str(account.shell)
	attrs['nid'] = str(account.nid)

	ldif = modlist.addModlist(attrs)
	con = open_connection()

	try:
		dn = "uid=" + attrs['uid'] + ",ou=People,dc=linux,dc=ime,dc=usp,dc=br"
		con.add_s(dn, ldif)
	except:
		return False
	return True

def find_group_by_gid(gid):
	try:
		return query('ou=Group', 'gidNumber=%s' % gid)[0][1]
	except:
		return None

def find_group_by_name(name):
	try:
		return query('ou=Group', 'cn=%s' % name)[0][1]
	except:
		return None

def find_grupo_by_gid(gid):
	return find_group_by_gid(gid)

def find_grupo_by_name(name):
	return find_group_by_name(name)

def get_gid(curso):
	try:
		return find_grupo_by_name(curso)['gidNumber'][0]
	except:
		return -1

def change_password(login, password):
	import os
	command = "ldappasswd -D "+ROOTDN+" -w"+ROOTPW+" uid=" + login + ",ou=People," + BASEDN + " -s" + password
	return os.system(command)

def remove_password(login):
	dn = "uid=" + str(login) + ",ou=People," + BASEDN
	con = open_connection()
	try:
		con.modify_s( dn, [ (ldap.MOD_DELETE, 'userPassword', None) ])
		return True
	except ldap.NO_SUCH_OBJECT:
		return False

def change_group(login, gid):
	dn = "uid=" + str(login) + ",ou=People," + BASEDN
	con = open_connection()
	try:
		con.modify_s( dn, [ (ldap.MOD_REPLACE, 'gidNumber', [str(gid)]) ] )
		return True
	except ldap.NO_SUCH_OBJECT:
		return False
	
def group_add_member(gname, login):
	dn = "cn=" + gname + ",ou=Group," + BASEDN
	con = open_connection()
	try:
		con.modify_s(dn, [ (ldap.MOD_ADD, 'memberUid', str(login)) ] )
		return True
	except ldap.NO_SUCH_OBJECT:
		return False

def group_remove_member(gname, login):
	dn = "cn=" + gname + ",ou=Group," + BASEDN
	con = open_connection()
	try:
		con.modify_s(dn, [ (ldap.MOD_DELETE, 'memberUid', str(login)) ] )
		return True
	except ldap.NO_SUCH_OBJECT:
		return False
	
