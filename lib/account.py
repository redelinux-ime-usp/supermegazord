# -*- coding: utf-8 -*-

# Account: Fornece a classe Account, que representa a conta de um usuário da rede 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-12

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()


class Account:
	def __init__(self, uid, gid, login, name, home, shell):
		self.uid = uid
		self.gid = gid
		self.login = login
		self.name = name
		self.home = home
		self.shell = shell
		self.password = ''
		self.nid = -1

	def set_nid(self, nid):
		self.nid = nid
		
	def set_password(self, password):
		self.password = password

	def add_to_ldap(self):
		import ldapwrap
		return ldapwrap.add_user(self)

	def is_in_group(self, gid):
		import ldapwrap
		group = ldapwrap
		return False


def from_ldap(ldapdata):
	uid = ldapdata['uidNumber'][0]
	gid = ldapdata['gidNumber'][0]
	login = ldapdata['uid'][0]
	name = ldapdata['cn'][0]
	home = ldapdata['homeDirectory'][0]
	shell = ldapata['loginShell'][0]
	return Account(uid, gid, login, name, home, shell)


