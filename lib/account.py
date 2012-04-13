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

	def add_to_kerberos(self):
		import kerbwrap
		return kerbwrap.add_user(self.name, self.password)

	def send_password_update(self):
		import kerbwrap
		return change_password(self.name, self.password)

	def is_in_group_by_ldapdata(self, group):
		if group['gidNumber'][0] == str(self.gid): return True
		if 'memberUid' not in group: return False
		return self.login in group['memberUid']
		
	def is_in_group_by_gid(self, gid):
		import ldapwrap
		return self.is_in_group_by_ldapdata(ldapwrap.find_grupo_by_gid(gid))

	def is_in_group_by_name(self, gname):
		import ldapwrap
		return self.is_in_group_by_ldapdata(ldapwrap.find_grupo_by_name(gname))
		

def from_ldap(ldapdata):
	try:
		uid = ldapdata['uidNumber'][0]
		gid = ldapdata['gidNumber'][0]
		login = ldapdata['uid'][0]
		if 'gecos' in ldapdata:
			name = ldapdata['gecos'][0]
		else:
			name = ldapdata['cn'][0]
		home = ldapdata['homeDirectory'][0]
		shell = ldapdata['loginShell'][0]
		return Account(uid, gid, login, name, home, shell)
	except:
		return None

def from_login(login):
	import ldapwrap
	return from_ldap(ldapwrap.find_user_by_login(login))
	

